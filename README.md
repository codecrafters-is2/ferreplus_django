# Ferreplus web app

### Configuración del SMTP
Para que el envío de emails funcione (sign-up, reset password), es necesario configurar las siguientes variables de entorno el archivo .env ubicado a nivel del directorio raíz del proyecto:
```
EMAIL_BACKEND=<email-backend> #'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=<host>
EMAIL_PORT=<port>
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<user>
EMAIL_HOST_PASSWORD=<pass>
DEFAULT_FROM_EMAIL=<sender>
```