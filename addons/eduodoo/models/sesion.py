# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Sesión (en realidad: Convocatoria/Edición del curso):
# Un curso puede abrir varias convocatorias (grupo tarde/mañana, fechas, plazas, profe...)
class EduodooSesion(models.Model):
    _name = "eduodoo.sesion"
    _description = "Convocatoria"

    name = fields.Char(string="Convocatoria", compute="_compute_name", store=True)

    # Fecha de inicio de la convocatoria (inicio del curso para ese grupo)
    fecha_inicio = fields.Datetime(string="Inicio", required=True)

    # Duración total del curso en esa convocatoria (ej: 40h)
    duracion_horas = fields.Float(string="Duración total (horas)", required=True, default=40.0)

    # Plazas disponibles para esa convocatoria
    asientos = fields.Integer(string="Plazas", required=True, default=15)

    # Curso base
    curso_id = fields.Many2one("eduodoo.curso", string="Curso", required=True, ondelete="restrict")

    # Grupo / horario (Mañana / Tarde / Grupo A...)
    clase_id = fields.Many2one("eduodoo.clase", string="Grupo / Horario", ondelete="restrict")

    # Profesor asignado a la convocatoria
    profesor_id = fields.Many2one("eduodoo.profesor", string="Profesor", ondelete="restrict")

    # Matrículas asociadas (quién se ha inscrito a esta convocatoria)
    matricula_ids = fields.One2many(
        comodel_name="eduodoo.matricula",
        inverse_name="sesion_id",
        string="Matrículas",
    )

    # Vista rápida de alumnos (derivada de matrículas)
    alumno_ids = fields.Many2many(
        comodel_name="eduodoo.alumno",
        string="Alumnos",
        compute="_compute_alumno_ids",
        store=False,
    )

    @api.depends("curso_id", "curso_id.name", "fecha_inicio", "clase_id", "clase_id.nombre")
    def _compute_name(self):
        for rec in self:
            partes = []

            curso_name = rec.curso_id.name if rec.curso_id and rec.curso_id.name else ""
            if curso_name:
                partes.append(str(curso_name))

            clase_name = rec.clase_id.nombre if rec.clase_id and rec.clase_id.nombre else ""
            if clase_name:
                partes.append(str(clase_name))

            if rec.fecha_inicio:
                partes.append(fields.Datetime.to_string(rec.fecha_inicio))

            rec.name = " - ".join(partes) if partes else "Convocatoria"


    @api.depends("matricula_ids.alumno_id")
    def _compute_alumno_ids(self):
        for rec in self:
            rec.alumno_ids = rec.matricula_ids.mapped("alumno_id")
