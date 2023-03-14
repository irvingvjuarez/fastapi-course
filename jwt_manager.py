from jwt import encode
from models.user import User

def create_token(data: User):
	token = encode(payload=data, key="my_secret_key", algorithm="HS256")
	return token