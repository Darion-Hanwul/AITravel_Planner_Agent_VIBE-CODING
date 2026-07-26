import re
import secrets
import string

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    """
    Mengubah password menjadi hash menggunakan bcrypt.

    Args:
        password (str): Password asli.

    Returns:
        str: Password yang telah di-hash.
    """
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

def validate_password_strength(
    password: str,
) -> tuple[bool, str]:

    if len(password) < 8:
        return False, "Password minimal 8 karakter."

    if not re.search(r"[A-Z]", password):
        return False, "Password harus memiliki huruf kapital."

    if not re.search(r"[a-z]", password):
        return False, "Password harus memiliki huruf kecil."

    if not re.search(r"[0-9]", password):
        return False, "Password harus memiliki angka."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password harus memiliki karakter spesial."

    return True, "Password valid."

def generate_random_password(
    length: int = 12,
) -> str:
    alphabet = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )