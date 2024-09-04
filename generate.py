import os
import base64

# Generate a random 32-byte key
key = os.urandom(32)

# Encode the key in Base64
base64_key = base64.b64encode(key).decode('utf-8')

print(f"Your Base64-encoded secret key: {base64_key}")
