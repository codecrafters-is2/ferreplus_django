# Ferreplus web app

### Setup del proyecto
```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    # Recordar setear las variables de entorno (más abajo)
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py create_user_groups  # Crear grupos para asignar a los usuarios
```
### Configuración del SMTP
Para que el envío de emails funcione (sign-up, reset password), es necesario configurar las siguientes variables de entorno el archivo .env ubicado a nivel del directorio raíz del proyecto:
```
EMAIL_BACKEND=<email-backend> #'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=<smtp-service-url>
EMAIL_PORT=<port/'587'(default)>
EMAIL_HOST_USER=<user-email-or-id>
EMAIL_HOST_PASSWORD=<api-or-app-key>
DEFAULT_FROM_EMAIL=<sender-email>  # Puede opmitirse en settings.py
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```