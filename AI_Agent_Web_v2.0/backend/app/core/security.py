import hashlib
import secrets

def sanitize_input(text: str) -> str:
    return text.strip()

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${hash_bytes.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, hash_hex = hashed.split('$')
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return hash_bytes.hex() == hash_hex
    except Exception:
        return False
