from flask import request, g
from models.user import User
from environment.config import secret 
from functools import wraps
import jwt 

def secure_route(func):
	@wraps(func)
	def wrapper(*args, **kwargs):

		row_token = request.headers['Authorization']
		clean_token = row_token.replace('Bearer ', '')

		try:
			payload = jwt.decode(clean_token, secret)
			user_id = payload['sub']
			user = User.query.get(user_id)

			if not user:
				return { 'message': 'Unauthorized User'}, 401 

			g.current_user = user 

		except jwt.ExpiredSignatureError:
			return { 'message': 'Expired token, Please login'}, 401

		except Exception:
			return { 'message': 'Unauthorized, An exception error occurred'}, 401

		return func(*args, **kwargs)
	return wrapper