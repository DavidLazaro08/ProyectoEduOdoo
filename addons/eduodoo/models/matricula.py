# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EduodooMatricula(models.Model):
    _name = "eduodoo.matricula"
    _description = "Matrícula"
    _rec_name = "name"

    name = fields.Char(string="Matrícula", compute="_compute_name", store=True)

    alumno_id = fields.Many2one("eduodoo.alumno", string="Alumno", required=True, ondelete="restrict")
    sesion_id = fields.Many2one("eduodoo.sesion", string="Sesión", required=True, ondelete="restrict")
    fecha_matricula = fields.Date(string="Fecha de matrícula", default=fields.Date.today)

    estado_pago = fields.Selection(
        selection=[("pendiente", "Pendiente"), ("pagada", "Pagada")],
        string="Estado de pago",
        required=True,
        default="pendiente",
    )

    # Facturas asociadas (en tu diseño será 0 o 1 por el unique de factura)
    factura_ids = fields.One2many(
        comodel_name="eduodoo.factura",
        inverse_name="matricula_id",
        string="Facturas",
    )

    @api.depends("alumno_id", "sesion_id")
    def _compute_name(self):
        for rec in self:
            alumno = rec.alumno_id.nombre if rec.alumno_id else ""
            sesion = rec.sesion_id.name if rec.sesion_id else ""
            rec.name = f"{alumno} - {sesion}" if (alumno or sesion) else "Matrícula"

    _sql_constraints = [
        ("matricula_unica", "unique(alumno_id, sesion_id)", "Este alumno ya está matriculado en esta sesión."),
    ]

    def action_crear_factura(self):
        self.ensure_one()

        # Si ya existe factura, abre esa
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

        # Crear factura nueva con cantidad por defecto = precio del curso
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
