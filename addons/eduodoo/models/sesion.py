# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


# Convocatoria (Sesión)
# Una convocatoria es una edición concreta de un curso: fechas, grupo/horario, plazas y profesor.
# De aquí cuelgan las matrículas y se calcula la ocupación.
#
# En el proyecto (por semanas):
# - Semana 1: modelo y relaciones (curso/grupo/profesor/matrículas).
# - Semana 2: ocupación (computados) y validaciones (plazas y solapes).
# - Semana 3: soporte para vistas avanzadas (fechas fin + acción de calendario por profesor).
class EduodooSesion(models.Model):
    _name = "eduodoo.sesion"
    _description = "Convocatoria"

    # Nombre calculado para que sea identificable en listas y búsquedas
    name = fields.Char(string="Convocatoria", compute="_compute_name", store=True)

    # Fechas de la convocatoria
    fecha_inicio = fields.Datetime(string="Inicio", required=True)
    duracion_horas = fields.Float(string="Duración total (horas)", required=True, default=40.0)
    fecha_fin = fields.Datetime(string="Fin", compute="_compute_fecha_fin", store=True)

    # Plazas disponibles
    asientos = fields.Integer(string="Plazas", required=True, default=15)

    # Relación con curso, grupo y profesor
    curso_id = fields.Many2one("eduodoo.curso", string="Curso", required=True, ondelete="restrict")
    clase_id = fields.Many2one("eduodoo.clase", string="Grupo / Horario", ondelete="restrict")
    profesor_id = fields.Many2one("eduodoo.profesor", string="Profesor", ondelete="restrict")

    # Matrículas asociadas a esta convocatoria
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

    # Ocupación
    plazas_ocupadas = fields.Integer(
        string="Plazas ocupadas",
        compute="_compute_ocupacion",
        store=True,
    )

    porcentaje_ocupacion = fields.Float(
        string="% Ocupación",
        compute="_compute_ocupacion",
        store=True,
        digits=(16, 2),
        group_operator=False,  # Es un porcentaje: no tiene sentido que se sume al agrupar
    )

    # Para pintar la sesión como “llena” en listas / embebidos
    esta_llena = fields.Boolean(
        string="Sesión llena",
        compute="_compute_ocupacion",
        store=True,
    )

    # -------------------------------------------------------------------------
    # Computes
    # -------------------------------------------------------------------------
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

    @api.depends("fecha_inicio", "duracion_horas")
    def _compute_fecha_fin(self):
        for rec in self:
            if rec.fecha_inicio:
                dur = rec.duracion_horas or 0.0
                rec.fecha_fin = rec.fecha_inicio + timedelta(hours=dur)
            else:
                rec.fecha_fin = False

    @api.depends("matricula_ids", "asientos")
    def _compute_ocupacion(self):
        """
        Calcula:
        - plazas_ocupadas: nº de matrículas
        - porcentaje_ocupacion: (ocupadas / asientos) * 100
        - esta_llena: True si ya no quedan plazas
        """
        for rec in self:
            ocupadas = len(rec.matricula_ids)
            rec.plazas_ocupadas = ocupadas

            if rec.asientos and rec.asientos > 0:
                rec.porcentaje_ocupacion = (ocupadas / rec.asientos) * 100.0
            else:
                rec.porcentaje_ocupacion = 0.0

            rec.esta_llena = bool(rec.asientos and ocupadas >= rec.asientos)

    # -------------------------------------------------------------------------
    # Validaciones
    # -------------------------------------------------------------------------
    @api.constrains("matricula_ids", "asientos")
    def _check_no_superar_asientos(self):
        for rec in self:
            if rec.asientos is not None and rec.asientos >= 0:
                if len(rec.matricula_ids) > rec.asientos:
                    raise ValidationError("No se puede superar el número de plazas disponibles en la sesión.")

    @api.constrains("profesor_id", "fecha_inicio", "duracion_horas")
    def _check_profesor_no_doble_sesion(self):
        """
        Evita que un profesor tenga dos convocatorias solapadas en el tiempo.
        Regla de solape:
          - (otra_inicio < fin_actual) AND (otra_fin > inicio_actual)
        """
        for rec in self:
            if not rec.profesor_id or not rec.fecha_inicio:
                continue

            dur = rec.duracion_horas or 0.0
            fin = rec.fecha_inicio + timedelta(hours=dur)

            # Buscamos otras sesiones del mismo profesor y comprobamos solape en Python (simple y claro)
            otras = self.search([
                ("profesor_id", "=", rec.profesor_id.id),
                ("id", "!=", rec.id),
                ("fecha_inicio", "!=", False),
            ])

            for otra in otras:
                otra_dur = otra.duracion_horas or 0.0
                otra_fin = otra.fecha_inicio + timedelta(hours=otra_dur)

                solapa = (otra.fecha_inicio < fin) and (otra_fin > rec.fecha_inicio)
                if solapa:
                    raise ValidationError(
                        "El profesor ya tiene otra sesión asignada que coincide en horario.\n"
                        f"- Sesión actual: {rec.name}\n"
                        f"- Sesión existente: {otra.name}"
                    )

    # -------------------------------------------------------------------------
    # Acciones
    # -------------------------------------------------------------------------
    def action_view_profesor_calendar(self):
        """
        Abre la vista de calendario de sesiones filtrada por el profesor de esta sesión.
        Si hay fecha de inicio, muestra un rango aproximado de ±30 días.
        """
        self.ensure_one()

        context = {
            "default_profesor_id": self.profesor_id.id,
            "search_default_profesor_id": self.profesor_id.id,
        }

        domain = [("profesor_id", "=", self.profesor_id.id)]

        if self.fecha_inicio:
            context["default_fecha_inicio"] = self.fecha_inicio
            context["initial_date"] = self.fecha_inicio.date()

            fecha_min = self.fecha_inicio - timedelta(days=30)
            fecha_max = self.fecha_inicio + timedelta(days=30)
            domain.extend([
                ("fecha_inicio", ">=", fecha_min),
                ("fecha_inicio", "<=", fecha_max),
            ])

        return {
            "type": "ir.actions.act_window",
            "name": f"Calendario de {self.profesor_id.nombre}",
            "res_model": "eduodoo.sesion",
            "view_mode": "calendar,list,form",
            "domain": domain,
            "context": context,
        }
