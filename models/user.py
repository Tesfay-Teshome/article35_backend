from app import db, bcrypt
from models.base import BaseModel
from datetime import *
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from environment.config import secret 
import jwt 
import re 

class User(db.Model, BaseModel):
	__tablename__ = 'users'

	username = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(130), nullable=False, unique=True)
	nikename = db.Column(db.String(130), nullable=False)
	phonenumber = db.Column(db.Integer(20), nullable=False unique=True)
	password_hash = db.Column(db.String(130), nullable=False)
	confirm_password_hash = db.Column(db.String(130), nullable=False)
	age = db.Column(db.Integer(10), nullable=False)

    @hybrid_property
    def password(self):
	    pass

    @password.setter
    def password(self, password_plaintext):
	    if not re.match('^(?=.*\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{5,20}$', password_plaintext):
		    raise AssertionError('Password must contain at least 1 capital, 1 number, 1 symbol, and be between 5 and 20 charetars long.')
	    self.password_hash = bcrypt.generate_password_hash(password_plaintext).decode('utf-8')
	    self.confirm_password_hash = bcrypt.generate_password_hash(password_plaintext).decode('utf-8')


    def validate_password(self, password_plaintext):
	    return bcrypt.check_password_hash(self.password_hash, self.confirm_password_hash, password_plaintext)

	def generate_token(self):
		payload = {
		'exp' : datetime.utcnow() + timedelta(days=1),
		'iat' : datetime.utcnow(),
		'sub' : self.id
		}

		token = jwt.encode(
			payload,
			secret,
			'HS256'
			).decode('utf-8')

		return token
	@validates('username')
	def validate_username(self, key, username):
		if not username:
			raise AssertionError('No username provided')
		if len(username) < 2 or len(username) > 20:
			raise AssertionError('Username must be between 2 and 20 characters')
		if password_hash != confirm_password_hash:
			raise AssertionError('Passwords must be equal!')
		return username

	@validates('email')
	def validate_email(self, key, email):
		if not email:
			raise AssertionError('No Email Provided')
		if User.query.filter(User.email == email).first():
			raise AssertionError('Email is already in use!')
		if not re.match("@]+@[^@]+\.[^@]+", email):
			raise AssertionError('Provided email is not valid Email address!')
		return email