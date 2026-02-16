# -*- coding: utf-8 -*-
{
    "name": "EduOdoo",
    "summary": "Sistema integral de gestión para una academia de cursos",
    "description": """
EduOdoo es un módulo Odoo para gestionar una academia de cursos.
Incluye la gestión de:
- Cursos y convocatorias (sesiones)
- Alumnos y matrículas
- Profesores y asignación de sesiones
- Facturas asociadas a matrículas
- Vistas avanzadas (calendario y kanban) para planificación
    """,
    "author": "David Gutiérrez",
    "website": "",
    "category": "Education",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "eduodoo/static/src/css/eduodoo_backend.css",
        ],
    },
    "installable": True,
    "application": True,
}
