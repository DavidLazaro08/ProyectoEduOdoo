# -*- coding: utf-8 -*-
from odoo import models, fields

# Alumno: datos básicos + matrículas (inscripciones a sesiones).
class EduodooAlumno(models.Model):
    _name = "eduodoo.alumno"
    _description = "Alumno"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    email = fields.Char(string="Email")

    matricula_ids = fields.One2many(
        comodel_name="eduodoo.matricula",
        inverse_name="alumno_id",
        string="Matrículas",
    )
