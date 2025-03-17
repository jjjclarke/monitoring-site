import hashlib

def get_secret_key():
    with open('key.txt', 'r') as file:
        return file.read().strip()

def get_password_hash():
    with open('secrets.txt', 'r') as file:
        return file.read().strip()
    
def verify_password(input_password):
    input_password_hash = hashlib.sha256(input_password.encode()).hexdigest()
    stored_password_hash = get_password_hash()
    
    return input_password_hash == stored_password_hash