from jwt import encode, decode
from models.user import User
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer

def create_token(data: User):
	token = encode(payload=data, key="my_secret_key", algorithm="HS256")
	return token

def validate_token(token: str):
	data: dict = decode(token, key="my_secret_key", algorithms=["HS256"])
	return data

class JWTBearer(HTTPBearer):
	async def __call__(self, request: Request):
		auth = await super().__call__(request)
		data = validate_token(auth.credentials)

		if data["email"] != "admin@gmail.com":
			raise HTTPException(status_code=403, detail="Invalid credentials")