import secrets
import base64

# Generate a secure random key
secret_key = secrets.token_hex(32)
print("\nGenerated SECRET_KEY:")
print("=" * 50)
print(secret_key)
print("=" * 50)

# Also generate a URL-safe base64 encoded version
url_safe_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
print("\nAlternative URL-safe SECRET_KEY:")
print("=" * 50)
print(url_safe_key)
print("=" * 50)
