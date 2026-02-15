# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


# Matrícula
# Une a un alumno con una convocatoria (sesión). Aquí gestionamos el flujo de estado
# (borrador -> confirmada -> pagada), la sincronía con el estado de pago y la factura.
#
# En el proyecto (por semanas):
# - Semana 1: modelo y relaciones (alumno/sesión/facturas).
# - Semana 2: flujo de estados, validación de plazas y creación/consulta de factura.
class EduodooMatricula(models.Model):
    _name = "eduodoo.matricula"
    _description = "Matrícula"
    _rec_name = "name"

    # Nombre calculado para identificar la matrícula fácilmente
    name = fields.Char(string="Matrícula", compute="_compute_name", store=True)

    # -------------------------------------------------------------------------
    # Flujo de estados
    # -------------------------------------------------------------------------
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("confirmada", "Confirmada"),
            ("pagada", "Pagada"),
        ],
        string="Estado",
        default="draft",
        required=True,
    )

    alumno_id = fields.Many2one("eduodoo.alumno", string="Alumno", required=True, ondelete="restrict")
    sesion_id = fields.Many2one("eduodoo.sesion", string="Sesión", required=True, ondelete="restrict")
    fecha_matricula = fields.Date(string="Fecha de matrícula", default=fields.Date.today)

    # Estado de pago (se mantiene separado del estado del flujo)
    estado_pago = fields.Selection(
        selection=[("pendiente", "Pendiente"), ("pagada", "Pagada")],
        string="Estado de pago",
        required=True,
        default="pendiente",
    )

    # Facturas asociadas (normalmente 0 o 1)
    factura_ids = fields.One2many(
        comodel_name="eduodoo.factura",
        inverse_name="matricula_id",
        string="Facturas",
    )

    # -------------------------------------------------------------------------
    # Computes / restricciones
    # -------------------------------------------------------------------------
    @api.depends("alumno_id", "sesion_id")
    def _compute_name(self):
        for rec in self:
            alumno = rec.alumno_id.nombre if rec.alumno_id else ""
            sesion = rec.sesion_id.name if rec.sesion_id else ""
            rec.name = f"{alumno} - {sesion}" if (alumno or sesion) else "Matrícula"

    _sql_constraints = [
        ("matricula_unica", "unique(alumno_id, sesion_id)", "Este alumno ya está matriculado en esta sesión."),
    ]

    # -------------------------------------------------------------------------
    # Validación de plazas
    # -------------------------------------------------------------------------
    @api.constrains("sesion_id")
    def _check_sesion_con_plazas(self):
        for rec in self:
            if not rec.sesion_id:
                continue

            sesion = rec.sesion_id
            # Contamos las matrículas actuales de esa sesión (incluye la presente si ya está guardada)
            total = self.search_count([("sesion_id", "=", sesion.id)])

            if sesion.asientos is not None and sesion.asientos >= 0:
                if total > sesion.asientos:
                    raise ValidationError("No quedan plazas disponibles en esta sesión.")

    # -------------------------------------------------------------------------
    # Sincronía simple entre flujo y pago
    # -------------------------------------------------------------------------
    @api.onchange("state")
    def _onchange_state_sync_pago(self):
        for rec in self:
            rec.estado_pago = "pagada" if rec.state == "pagada" else "pendiente"

    @api.onchange("estado_pago")
    def _onchange_pago_sync_state(self):
        for rec in self:
            if rec.estado_pago == "pagada":
                rec.state = "pagada"
            elif rec.state == "pagada":
                rec.state = "confirmada"

    # -------------------------------------------------------------------------
    # Acciones del flujo (botones)
    # -------------------------------------------------------------------------
    def action_confirmar(self):
        for rec in self:
            rec.state = "confirmada"
            rec.estado_pago = "pendiente"

    def action_marcar_pagada(self):
        for rec in self:
            rec.state = "pagada"
            rec.estado_pago = "pagada"

    # -------------------------------------------------------------------------
    # Factura: crear o abrir la existente
    # -------------------------------------------------------------------------
    def action_crear_factura(self):
        self.ensure_one()

        factura_existente = self.env["eduodoo.factura"].search([("matricula_id", "=", self.id)], limit=1)
        if factura_existente:
            return {
                "type": "ir.actions.act_window",
                "name": "Factura",
                "res_model": "eduodoo.factura",
                "view_mode": "form",
                "res_id": factura_existente.id,
                "target": "current",
            }

        cantidad = 0.0
        concepto = ""

        if self.sesion_id and self.sesion_id.curso_id:
            cantidad = self.sesion_id.curso_id.price or 0.0
            concepto = self.sesion_id.curso_id.name or ""

        factura = self.env["eduodoo.factura"].create({
            "matricula_id": self.id,
            "cantidad": cantidad,
            "concepto": concepto,
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Factura",
            "res_model": "eduodoo.factura",
            "view_mode": "form",
            "res_id": factura.id,
            "target": "current",
        }
