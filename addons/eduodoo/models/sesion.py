# -*- coding: utf-8 -*-
from odoo import models, fields


class EduodooSesion(models.Model):
    _name = "eduodoo.sesion"
    _description = "Sesión"

    start_datetime = fields.Datetime(string="Inicio", required=True)
    duration_hours = fields.Float(string="Duración (horas)", required=True, default=1.0)
    seats = fields.Integer(string="Asientos", required=True, default=1)

    course_id = fields.Many2one(
        comodel_name="eduodoo.curso",
        string="Curso",
        required=True,
        ondelete="restrict",
    )
