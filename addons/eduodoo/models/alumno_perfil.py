# -*- coding: utf-8 -*-
from odoo import models, fields

# Perfil extendido del alumno (simula One2One: un alumno - un perfil, gracias a UNIQUE).
class EduodooAlumnoPerfil(models.Model):
    _name = "eduodoo.alumno_perfil"
    _description = "Perfil de Alumno"
    _rec_name = "dni" 

    alumno_id = fields.Many2one(
        comodel_name="eduodoo.alumno",
        string="Alumno",
        required=True,
        ondelete="cascade",
    )

    telefono = fields.Char(string="Teléfono")
    dni = fields.Char(string="DNI")
    direccion = fields.Char(string="Dirección")

    _sql_constraints = [
        ("alumno_unique", "unique(alumno_id)", "Este alumno ya tiene un perfil."),
    ]
