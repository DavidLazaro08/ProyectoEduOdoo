# -*- coding: utf-8 -*-
from odoo import models, fields

# Profesor: datos básicos + cursos que puede impartir + sesiones asignadas.
class EduodooProfesor(models.Model):
    _name = "eduodoo.profesor"
    _description = "Profesor"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    titulacion = fields.Char(string="Titulación")

    curso_ids = fields.Many2many(
        comodel_name="eduodoo.curso",
        relation="eduodoo_profesor_curso_rel",
        column1="profesor_id",
        column2="curso_id",
        string="Cursos que imparte",
    )

    sesion_ids = fields.One2many(
        comodel_name="eduodoo.sesion",
        inverse_name="profesor_id",
        string="Sesiones",
    )
