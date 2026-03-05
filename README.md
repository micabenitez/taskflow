# 📋 Kanban REST API - Backend Server

Una API RESTful robusta y escalable construida para gestionar tableros Kanban. Diseñada bajo una arquitectura orientada a servicios (SaaS), soporta multi-tenancy donde cada usuario tiene acceso aislado y seguro a sus propios tableros y tareas.

## Tecnologías y Stack

* **Lenguaje:** Python 3
* **Framework:** Django & Django REST Framework (DRF)
* **Base de Datos:** PostgreSQL (Desplegada en la nube vía Neon/AWS)
* **Autenticación:** JSON Web Tokens (JWT) vía `SimpleJWT`
* **Testing:** `unittest` nativo de Django (Unit & Integration Tests)

## Buenas Prácticas Aplicadas

* Modelado de datos relacional (1:N) con un diseño claro de entidades (`Board`, `Column`, `Card`).
* Endpoints protegidos por JWT. Aislamiento de datos a nivel de consulta (`get_queryset`) para garantizar que un usuario no pueda acceder a recursos de terceros.
* Optimización de peticiones HTTP al devolver estructuras de datos completas en un solo llamado al servidor, reduciendo el *over-fetching*.