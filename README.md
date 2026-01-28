# ProyectoEduOdoo (Odoo 18) – David Gutiérrez

Proyecto incremental por semanas para modelado y desarrollo en Odoo.

## Estructura
- `addons/eduodoo/` → módulo principal del proyecto

## Arranque (local)
Ejemplo (adaptar a tu odoo.conf):
- Ejecutar Odoo con el archivo de configuración:
  - `python odoo-bin -c odoo.conf --dev=all`

## Semana 26–30 enero
- Modelos: Curso, Sesión, Alumno, Clases, Facturación, Profesor
- Relaciones: Many2one, Many2many, One2One
- Entrega: tablas en PostgreSQL + modelos visibles en Odoo (modo técnico)
