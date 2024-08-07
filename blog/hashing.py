import passlib.context

#hash passwords
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(passwod:str):
        return pwd_context.hash(passwod)
    
    def verify_pass(hashed_pass, plain_pass):
        return pwd_context.verify(plain_pass, hashed_pass)