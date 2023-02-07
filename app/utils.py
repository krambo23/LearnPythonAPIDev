from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(inputted_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(inputted_password, hashed_password)
