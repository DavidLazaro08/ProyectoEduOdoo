# -*- coding: utf-8 -*-
from odoo import fields, models


# Clase / Grupo
# Representa un grupo o turno (mañana, tarde, grupo A...) al que se asignan convocatorias.
#
# En el proyecto:
# - Semana 1: definición del modelo y relación con sesiones.
class EduodooClase(models.Model):
    _name = "eduodoo.clase"
    _description = "Clase / Grupo"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    horario = fields.Char(string="Horario")

    # Sesiones (convocatorias) que pertenecen a este grupo/turno
    sesion_ids = fields.One2many(
        comodel_name="eduodoo.sesion",
        inverse_name="clase_id",
        string="Sesiones",
    )
