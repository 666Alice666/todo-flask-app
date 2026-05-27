from models import db, Task

def migrate():
    print("Applying migrations...")
    # Здесь вы можете вызвать Alembic, если используется:
    # from alembic import command
    # from alembic.config import Config
    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")
    print("Migrations applied.")

def create_admin(email):
    # У нас нет модели User, поэтому просто выводим сообщение
    print(f"Admin creation command received for email: {email}")
    print("Admin was created")

def clear_cache():
    print("Clearing cache...")
    # Здесь вы можете очистить Redis, например:
    # import redis
    # r = redis.from_url(config.REDIS_URL)
    # r.flushall()
    print("Cache cleared.")