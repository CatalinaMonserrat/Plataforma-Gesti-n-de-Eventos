# Plataforma de Gestión de Eventos (Django)

Proyecto desarrollado en **Django 5.2** como ejercicio de autenticación, autorización y gestión de roles.  
La aplicación permite registrar usuarios, crear y administrar eventos, y controlar el acceso según el rol del usuario (Administrador, Organizador o Asistente).

---

##  Instalación y configuración

1. Clonar el repositorio
   ```bash
   git clone https://github.com/TU_USUARIO/plataforma_gestion_eventos.git
   cd plataforma_gestion_eventos
2. Crear y activar entorno virtual
```bash
python -m venv myenv
myenv\Scripts\activate   # Windows
source myenv/bin/activate # Linux/Mac
```
3. Instalar dependencias
```bash
Copiar código
pip install -r requirements.txt
```
4. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```
6. Ejecutar servidor
```bash
python manage.py runserver
```
Accede en: http://127.0.0.1:8000

## Funcionalidades
- **Registro e inicio/cierre de sesión**
- **Roles y permisos**
  - **Administradores**: crear, editar y eliminar cualquier evento.
  - **Organizadores**: crear eventos y editar los propios, asignar asistentes.
  - **Asistentes**: solo pueden ver los eventos donde están registrados.
- **Gestión de eventos**: crear, listar, editar, eliminar.
- **Acceso denegado**: página de error personalizada con mensajes amigables.
- **Mensajes de éxito/error** usando el sistema `messages` de Django.
- **Bootstrap 5** para la interfaz (navbar, formularios, botones, alertas).

## Usuarios de prueba
Se incluyen 3 usuarios de ejemplo creados vía shell:

**Administrador**  
usuario: `admin1`  
clave: `admin123`  

**Organizador**  
usuario: `orga1`  
clave: `orga123`  

**Asistente**  
usuario: `asis1`  
clave: `asis123`

## Estructura del proyecto
```bash
plataforma_gestion_eventos/
│
├── eventos/           # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── gestion/           # App principal
│   ├── models.py      # Modelo Evento
│   ├── views.py       # CRUD + mixins de permisos
│   ├── forms.py       # Formularios (login, registro, evento)
│   ├── urls.py
│   └── templates/
│
├── db.sqlite3         # Base de datos (ignorada en .gitignore)
├── manage.py
└── requirements.txt
```
## Notas de seguridad
Este proyecto está configurado en modo DEBUG=True.
Para producción, en settings.py configurar:
```bash
python
Copiar código
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
## Licencia
Proyecto con fines educativos.
Desarrollado en el marco de Bootcamp Talento Digital.
