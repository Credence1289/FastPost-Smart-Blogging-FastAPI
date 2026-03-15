from datetime import timedelta, datetime
from jose import jwt, JWTError
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MIN = 30

def create_access_token(
        user_id : int,
        role : str,
        expiry : timedelta = None,
        refresh : bool = False
):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + (
            expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN)
        ),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    return token

def decode_token(token : str)->dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        return payload
    except JWTError:
        return None
