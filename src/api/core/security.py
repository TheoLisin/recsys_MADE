import bcrypt


def get_password_hash(password: str) -> str:
    bpass = bytes(password, "UTF-8")
    salt = bcrypt.gensalt()
    bytes_pwdhash = bcrypt.hashpw(bpass, salt)
    return bytes_pwdhash.decode("utf-8")
    

def verify_password(password: str, hashed_password: str) -> bool:
    bpass = bytes(password, "UTF-8")
    bpwd_hash = bytes(hashed_password, "UTF-8")
    return bcrypt.checkpw(bpass, bpwd_hash)
