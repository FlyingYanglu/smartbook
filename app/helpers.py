import hashlib

SECRET_KEY = "92312se"

def generate_signature(data):
    """Generate an MD5 signature using request data."""
    raw_string = f"{data['system_time'][:10]}|{SECRET_KEY}|{data['user_id'][3:-1]}|{data['sig_version']}"
    return hashlib.md5(raw_string.encode()).hexdigest()
