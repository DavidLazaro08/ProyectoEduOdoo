# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Factura: registro simple de pago asociado a una matrícula.
class EduodooFactura(models.Model):
    _name = "eduodoo.factura"
    _description = "Factura"
    _rec_name = "name"

    name = fields.Char(string="Factura", compute="_compute_name", store=True)

    matricula_id = fields.Many2one(
        comodel_name="eduodoo.matricula",
        string="Matrícula",
        required=True,
        ondelete="restrict",
    )

    # Campos "relacionados" para no duplicar datos:
    alumno_id = fields.Many2one(
        comodel_name="eduodoo.alumno",
        string="Alumno",
        related="matricula_id.alumno_id",
        store=True,
        readonly=True,
    )

    sesion_id = fields.Many2one(
        comodel_name="eduodoo.sesion",
        string="Sesión",
        related="matricula_id.sesion_id",
        store=True,
        readonly=True,
    )

    cantidad = fields.Float(string="Cantidad", required=True, default=0.0)
    fecha_pago = fields.Date(string="Fecha de pago")  # editable
    concepto = fields.Char(string="Concepto")

    _sql_constraints = [
        ("factura_matricula_unica", "unique(matricula_id)", "Esta matrícula ya tiene una factura."),
    ]

    @api.depends(
        "matricula_id.name",
        "fecha_pago",
        "alumno_id.nombre",
        "alumno_id.apellidos",
        "sesion_id.name",
    )
    def _compute_name(self):
        for rec in self:
            base = rec.matricula_id.name or "Factura"
            if rec.fecha_pago:
                rec.name = f"{base} ({rec.fecha_pago})"
            else:
                rec.name = base
