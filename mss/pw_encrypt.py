# encrypt using PBKDF2
# using: pip install passlib
from passlib.context import CryptContext

# create context with PBKDF2
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000  # -!- if wait time is too long reduce number of rounds -!-
)


# encrypt
def encrypt_password(password):
    return pwd_context.encrypt(password)


# -- TO ENCRYPT--
# before storing to database:
#       encrypt_password()


# verify
def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)
# -- TO VERIFY--
# after user enters password to login:
#       check_encrypted_password()
