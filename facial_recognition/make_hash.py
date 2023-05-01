# Make hash

# the file is used to convert the user passwords into a hash 
import hashlib

# the hash is used for password matching
# the project utilized sha256 as the primary hashing algorithm.
# Andvanced algorithms like DES and AES can be employed to further bolster security
def hash_password(password: str) -> str:
    """
    Hash a given password using SHA-256.
    """
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()
