# -*- coding: utf-8 -*-
from odoo import fields, models


# Alumno
# Guarda los datos básicos del alumno y sus matrículas (inscripciones) a convocatorias.
#
# En el proyecto:
# - Semana 1: definición del modelo y relación con matrículas.
class EduodooAlumno(models.Model):
    _name = "eduodoo.alumno"
    _description = "Alumno"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    email = fields.Char(string="Email")

    # Matrículas del alumno en distintas sesiones
    matricula_ids = fields.One2many(
        comodel_name="eduodoo.matricula",
        inverse_name="alumno_id",
        string="Matrículas",
    )
