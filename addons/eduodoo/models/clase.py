# -*- coding: utf-8 -*-
from odoo import models, fields

# Clase/Grupo: representa un turno/grupo y cuelgan sesiones de aquí.
class EduodooClase(models.Model):
    _name = "eduodoo.clase"
    _description = "Clase / Grupo"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True)
    horario = fields.Char(string="Horario")

    sesion_ids = fields.One2many(
        comodel_name="eduodoo.sesion",
        inverse_name="clase_id",
        string="Sesiones",
    )
