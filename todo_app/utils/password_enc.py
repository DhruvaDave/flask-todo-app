import hashlib

from todo_app.common.constants import UTF_ENCODING


def generate_password_hash(obj):
    """
    Hashes given object with hashlib.sha224 algorithm. Return string.
    """
    return hashlib.sha256(str(obj).encode(UTF_ENCODING)).hexdigest()
