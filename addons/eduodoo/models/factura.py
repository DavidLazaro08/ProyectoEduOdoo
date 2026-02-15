# -*- coding: utf-8 -*-
from odoo import api, fields, models


# Factura
# Registro simple de pago asociado a una matrícula. No pretende ser contabilidad real,
# solo una forma de dejar constancia del cobro dentro del módulo.
#
# En el proyecto (por semanas):
# - Semana 1: modelo y relaciones (matrícula / alumno / sesión).
# - Semana 2: restricción de “una factura por matrícula” y nombre calculado.
class EduodooFactura(models.Model):
    _name = "eduodoo.factura"
    _description = "Factura"
    _rec_name = "name"

    # Nombre calculado para que sea identificable en listados
    name = fields.Char(string="Factura", compute="_compute_name", store=True)

    matricula_id = fields.Many2one(
        comodel_name="eduodoo.matricula",
        string="Matrícula",
        required=True,
        ondelete="restrict",
    )

    # Datos derivados de la matrícula (para evitar duplicar y tener filtros cómodos)
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
    fecha_pago = fields.Date(string="Fecha de pago")
    concepto = fields.Char(string="Concepto")

    _sql_constraints = [
        ("factura_matricula_unica", "unique(matricula_id)", "Esta matrícula ya tiene una factura."),
    ]

    # -------------------------------------------------------------------------
    # Compute
    # -------------------------------------------------------------------------
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
            rec.name = f"{base} ({rec.fecha_pago})" if rec.fecha_pago else base
