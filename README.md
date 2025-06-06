Leasy Challenge
Este proyecto es un sistema de gestión de contratos, clientes y vehículos, desarrollado con Django, que permite cargar información desde archivos .csv y .xlsx, generar facturas automáticas y ejecutar tareas en segundo plano con django_rq.

Podes ver el proyecto en:
URL: https://leasy-challenge-app-02fbb54b6964.herokuapp.com/

Si queres verlo en local:
Instalación
Requerimientos
•	Python 3.12
•	Docker & Docker Compose
•	PostgreSQL 15
•	Redis 7
1.	Clonar el repositorio (en bash):
git clone https://github.com/facundoaguilera/leasy_challenge.git

2.	Configurar variables de entorno:
Crear un archivo .env con las siguientes variables:
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=leasydb
POSTGRES_USER=leasyuser
POSTGRES_PASSWORD=leasypass
DATABASE_URL=postgres://leasyuser:leasypass@db:5432/leasydb
3.	Construir y levantar los servicios:
bash
docker compose up –build
Esto crea migraciones, un cronjob para generar invoices automaticos y usuarios de prueba.
USUARIOS DE PRUEBA: 
ventas_user@leasy.test, con permiso de Ventas
operaciones_user@leasy.test, con permiso de Operciones
cobranzas_user@leasy.test, con permiso de Cobranzas
password: leasy1234 para estos ultimos 3.
admin@leasy.test, con permiso para todo, con password: admin123

Ejecución
Web App
•	Accede desde: http://localhost:8000
