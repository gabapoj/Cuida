import hashlib
import hmac
import secrets


def generate_secure_token(nbytes: int = 32) -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(nbytes)


def hash_token(token: str, secret_key: str) -> str:
    """HMAC-SHA256 hash of a token. Used to store tokens securely."""
    return hmac.new(
        secret_key.encode(),
        token.encode(),
        hashlib.sha256,
    ).hexdigest()
