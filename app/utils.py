from passlib.context import CryptContext

# Password Hashing
password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# To verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

# Convert Plain Password -> Hashed Password
def get_password_hash(password: str) -> str:
    return password_context.hash(password)
