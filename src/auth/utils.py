from passlib.context import CryptContext

password_contect = CryptContext(
   schemes=['bcrypt']
)


def generate_password_hash(password: str) -> str:
   hash = password_contect.hash(password)

   return hash

def verify_password(password: str, hash: str) -> bool:
   return password_contect.verify(password , hash)