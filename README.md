# EduOdoo - Sistema de Gestión Académica

Módulo de Odoo 18 diseñado para la gestión integral de una academia de formación.
Desarrollo incremental realizado por **David Gutiérrez**.

## Funcionalidades Principales

### Semana 1: Estructura de Datos
Definición de los modelos base del negocio:
- **Cursos:** Oferta formativa con niveles (A1-C2) y precios.
- **Sesiones:** Convocatorias concretas con fechas y profesores asignados.
- **Alumnos y Profesores:** Gestión de personas y titulaciones.
- **Matrículas y Facturación:** Flujo completo de inscripción y cobro.

### Semana 2: Lógica de Negocio
Automatización y restricciones para la integridad de los datos:
- **Cálculo de Ocupación:** Barra de progreso automática en sesiones.
- **Flujo de Matrícula:** Estados controlados (Borrador → Confirmada → Pagada).
- **Control de Facturación:** Generación automática y validación de cobros.

### Semana 3: Experiencia de Usuario (UX/UI)
Mejora visual mediante vistas avanzadas personalizadas:
- **Vista Calendario:** Planificación visual con códigos de color por profesor.
- **Vista Kanban:** Tarjetas informativas con indicador visual de ocupación y etiquetas de estado ("LLENA").
- **Estilos Corporativos:** Interfaz limpia y coherente (`eduodoo_backend.css`).

---

## Documentación Técnica: Restricciones Solucionadas

Tal como se solicita en el proyecto, se detallan las restricciones (`@api.constrains`) implementadas para garantizar la calidad del dato:

### 1. No permitir sobreventa de plazas
**Método:** `_check_no_superar_asientos` (Modelo `eduodoo.sesion`)
**Solución:** Se compara el número total de matrículas confirmadas con el campo `asientos` de la sesión. Si se supera el límite, el sistema bloquea la operación lanzando un `ValidationError`.

### 2. Evitar duplicidad de horario por profesor
**Método:** `_check_profesor_no_doble_sesion` (Modelo `eduodoo.sesion`)
**Solución:** Al asignar una sesión, el sistema busca automáticamente otras sesiones del mismo profesor que se solapen en el rango temporal `[fecha_inicio, fecha_fin]`. Si detecta coincidencia, impide la asignación para evitar conflictos de agenda.

---

## Instalación

1. Clonar este repositorio en tu directorio de `addons`.
2. Actualizar la lista de aplicaciones en Odoo (modo desarrollador).
3. Instalar/Actualizar el módulo **EduOdoo**.
