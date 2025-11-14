import hashlib
import uuid
from src.db.redis import redis_client
from src.core.config import settings

SESSION_PREFIX = "email-api:"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def generate_session_token() -> str:
    return hashlib.sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()

def save_session(token: str, username: str):
    redis_client.set(f"{SESSION_PREFIX}{token}", username, ex=settings.session_duration)

def get_session_username(token: str) -> str | None:
    username = redis_client.get(f"{SESSION_PREFIX}{token}")
    if username:
        return username.removeprefix(SESSION_PREFIX)
    return None

def delete_session(token: str):
    return redis_client.delete(f"{SESSION_PREFIX}{token}")
