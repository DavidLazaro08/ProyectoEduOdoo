# -*- coding: utf-8 -*-
from odoo import models, fields


class EduodooCurso(models.Model):
    _name = "eduodoo.curso"
    _description = "Curso"

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    level = fields.Selection(
        selection=[
            ("a1", "A1"),
            ("a2", "A2"),
            ("b1", "B1"),
            ("b2", "B2"),
            ("c1", "C1"),
            ("c2", "C2"),
        ],
        string="Nivel",
        required=True,
        default="a1",
    )
    price = fields.Float(string="Precio", required=True, default=0.0)
