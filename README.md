🏋️ Sistema de Gestión de Gimnasio

Aplicación web desarrollada con Python, Streamlit, SQLAlchemy y Supabase para administrar un gimnasio de forma sencilla e intuitiva.

El sistema permite gestionar socios, profesores, actividades deportivas, horarios, inscripciones y asistencias, centralizando toda la información en una base de datos PostgreSQL alojada en Supabase.

🚀 Características Principales
👥 Gestión de Socios
Alta de nuevos socios.
Registro de datos personales.
Consulta de información almacenada.
Eliminación de socios y registros asociados.
👨‍🏫 Gestión de Profesores
Registro de profesores.
Asociación de profesores a clases y actividades.
🏋️ Gestión de Actividades
Creación de actividades deportivas.
Configuración de duración y cupo máximo.
Administración de disciplinas del gimnasio.
📅 Gestión de Clases
Creación de horarios semanales.
Asociación entre actividad y profesor.
Validación para evitar horarios duplicados.
📋 Inscripciones
Inscripción fija de socios a actividades.
Control automático de vacantes.
Restricción de inscripciones duplicadas.
📝 Registro de Asistencias
Registro diario de asistencia.
Control de cupo por actividad.
Validación para evitar registros duplicados.
🗑️ Administración
Baja de socios.
Cancelación de inscripciones.
Eliminación de clases programadas.
🛠️ Tecnologías Utilizadas
Python
Streamlit
SQLAlchemy
PostgreSQL
Supabase
Psycopg2
🗄️ Modelo de Datos

El sistema está compuesto por las siguientes entidades principales:

Socio

Representa a los clientes del gimnasio.

Profesor

Representa a los instructores responsables de las actividades.

Actividad

Disciplina deportiva ofrecida por el gimnasio.

Clase

Horario específico asignado a una actividad y profesor.

Inscripción

Relación entre socios y actividades.

Asistencia

Registro diario de participación de los socios en clases.

📦 Instalación Local
1. Clonar el repositorio
git clone https://github.com/leomacrini/gimnasio.git
cd gimnasio
2. Crear entorno virtual
python -m venv venv
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
4. Configurar la conexión a Supabase

Crear un archivo de configuración o variables de entorno con los datos de conexión de PostgreSQL proporcionados por Supabase.

Ejemplo:

DB_HOST=xxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password
DB_PORT=5432
5. Ejecutar la aplicación
streamlit run app.py
☁️ Base de Datos

La aplicación utiliza:

PostgreSQL como motor de base de datos.
Supabase como servicio de alojamiento en la nube.

Ventajas:

Persistencia de datos.
Acceso remoto.
Escalabilidad.
Respaldo y administración simplificada.
🔒 Validaciones Implementadas
Documento único para socios.
Documento único para profesores.
Actividades sin nombres duplicados.
Control de cupos máximos.
Restricción de inscripciones repetidas.
Restricción de asistencias duplicadas.
Validación de horarios repetidos.
📈 Futuras Mejoras
Dashboard con estadísticas.
Gestión de cuotas y pagos.
Control de vencimientos.
Exportación de reportes PDF y Excel.
Autenticación de usuarios.
Roles de administrador y recepcionista.
Notificaciones automáticas.
👨‍💻 Autor

Leonardo Macrini

Desarrollado como proyecto de práctica para aplicar conceptos de:

Bases de Datos Relacionales
SQLAlchemy ORM
PostgreSQL
Streamlit
Arquitectura de aplicaciones CRUD

GitHub: https://github.com/leomacrini

📄 Licencia

Proyecto desarrollado con fines educativos y de aprendizaje.
