"""
Security Utilities

Berisi seluruh fungsi yang berkaitan dengan keamanan password.

Digunakan oleh:
- AuthService
- UserService
- Register API
- Change Password API
"""

import re
import secrets
import string

from passlib.context import CryptContext

# ==========================================================
# PASSWORD HASHING CONFIGURATION
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password: str) -> str:
    """
    Mengubah password menjadi hash menggunakan bcrypt.

    Args:
        password (str): Password asli.

    Returns:
        str: Password yang telah di-hash.
    """
    return pwd_context.hash(password)


# ==========================================================
# VERIFY PASSWORD
# ==========================================================

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Memverifikasi password.

    Args:
        plain_password (str): Password yang diinput user.
        hashed_password (str): Password hash dari database.

    Returns:
        bool
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# PASSWORD STRENGTH VALIDATION
# ==========================================================

def validate_password_strength(
    password: str,
) -> tuple[bool, str]:
    """
    Validasi kekuatan password.

    Rules:
    - Minimal 8 karakter
    - Minimal 1 huruf besar
    - Minimal 1 huruf kecil
    - Minimal 1 angka
    - Minimal 1 karakter spesial

    Returns:
        tuple[bool, str]
    """

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


# ==========================================================
# GENERATE RANDOM PASSWORD
# ==========================================================

def generate_random_password(
    length: int = 12,
) -> str:
    """
    Generate password acak.

    Args:
        length (int): Panjang password.

    Returns:
        str
    """

    alphabet = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )