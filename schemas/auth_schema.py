#schemas/auth_schema.py
import re
from pydantic import BaseModel, EmailStr, validator

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Şifre en az 8 karakter olmalıdır.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Şifre en az bir büyük harf içermelidir.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Şifre en az bir küçük harf içermelidir.")
        if not re.search(r"\d", value):
            raise ValueError("Şifre en az bir rakam içermelidir.")
        if not re.search(r"[!@#$%^&*()_\+\-=\[\]{}|;:'\",.<>?/]", value):
            raise ValueError("Şifre en az bir özel karakter içermelidir.")
        return value
    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class TokenResponce(BaseModel):
    access_token: str
    token_type: str