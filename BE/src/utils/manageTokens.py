import os
import jwt
import pytz
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from typing import Optional, Tuple

secret_key = os.getenv("SECRET_KEY", "default_secret_key")
algorithm = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: str) -> Optional[str]:
    try:
        expire_utc = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire_timestamp = int(expire_utc.timestamp())

        encoded_jwt = jwt.encode({"sub": email, "exp": expire_timestamp}, secret_key, algorithm=algorithm)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding token: {e}")
        return None


def decode_access_token(token: str) -> Optional[Tuple[str, str]]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm], leeway=10)

        email = payload.get("sub")
        exp_timestamp = payload.get("exp")

        if email is None or exp_timestamp is None:
            raise ValueError("Invalid token payload.")

        ist = pytz.timezone("Asia/Kolkata")
        expire_time = datetime.fromtimestamp(exp_timestamp, tz=ist).strftime("%Y-%m-%d %H:%M:%S %Z")

        return email, expire_time

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
