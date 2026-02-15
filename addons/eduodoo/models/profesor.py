# -*- coding: utf-8 -*-
from odoo import fields, models


# Profesor
# Guarda los datos básicos del profesor, los cursos que puede impartir
# y las sesiones (convocatorias) que tiene asignadas.
#
# En el proyecto:
# - Semana 1: definición del modelo y relación con sesiones.
# - Semana 3: uso como eje de visualización (agrupación y calendario).
class EduodooProfesor(models.Model):
    _name = "eduodoo.profesor"
    _description = "Profesor"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    titulacion = fields.Char(string="Titulación")

    # Cursos que el profesor puede impartir
    curso_ids = fields.Many2many(
        comodel_name="eduodoo.curso",
        relation="eduodoo_profesor_curso_rel",
        column1="profesor_id",
        column2="curso_id",
        string="Cursos que imparte",
    )

    # Sesiones asignadas al profesor
    sesion_ids = fields.One2many(
        comodel_name="eduodoo.sesion",
        inverse_name="profesor_id",
        string="Sesiones",
    )
