from datetime import datetime, timedelta, timezone
import jwt

ALGORITHM = "HS256"

def create_access_token(*, subject: str, secret_key: str, expires_minutes: int = 30) -> str:
    return create_token(subject=subject, secret_key=secret_key, expires_minutes=expires_minutes)

def create_refresh_token(*, subject: str, secret_key: str, expires_minutes: int) -> str:
    return create_token(subject=subject, secret_key=secret_key, expires_minutes=expires_minutes)

def create_token(*, subject: str, secret_key: str, expires_minutes: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)

def decode_token(token: str, secret_key: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
