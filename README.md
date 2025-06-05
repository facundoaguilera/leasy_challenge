Leasy Challenge
Este proyecto es un sistema de gestión de contratos, clientes y vehículos, desarrollado con Django, que permite cargar información desde archivos .csv y .xlsx, generar facturas automáticas y ejecutar tareas en segundo plano con django_rq.
Requerimientos
•	Python 3.12
•	Docker & Docker Compose
•	PostgreSQL 15
•	Redis 7
Instalación
1.	Clonar el repositorio (en bash):
git clone https://github.com/facundoaguilera/leasy_challenge.git
cd leasy_challenge
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
Los usuarios de prueba son ventas_user@leasy.test,  operaciones_user@leasy.test, cobranzas_user@leasy.test
password: leasy1234 y un usuario que tiene acceso a todos los grupos que es admin@test.com con password: admin123

Ejecución
Web App
•	Accede desde: http://localhost:8000
