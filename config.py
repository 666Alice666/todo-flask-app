import os
from decouple import config


def get_config():
    return {
        'SECRET_KEY': config('SECRET_KEY', default='a-very-secret-key'),
        'PORT': config('PORT', default=5000, cast=int),
        'DATABASE_URL': (
            f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
            f"@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
        ),
        'DEBUG': config('DEBUG', default=False, cast=bool),
    }


CONFIG = get_config()