"""from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check-posts-package-expiry': {
        'task': 'your_app_name.tasks.check_all_posts_package_expiry',
        'schedule': crontab(hour=0, minute=0),  # Ejecutar a medianoche todos los días
    },
}
"""