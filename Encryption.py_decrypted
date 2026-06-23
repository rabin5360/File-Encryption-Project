import os
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    # Convert password into a valid encryption key
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file(filepath, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(filepath, "rb") as f:
        original = f.read()

    encrypted = fernet.encrypt(original)

    encrypted_path = filepath + ".enc"
    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    print(f"[SUCCESS] File encrypted: {encrypted_path}")
    return encrypted_path

def decrypt_file(filepath, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(filepath, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        print("[ERROR] Wrong password or corrupted file!")
        return None

    # Remove the .enc extension
    decrypted_path = filepath.replace(".enc", "_decrypted")
    with open(decrypted_path, "wb") as f:
        f.write(decrypted)

    print(f"[SUCCESS] File decrypted: {decrypted_path}")
    return decrypted_path