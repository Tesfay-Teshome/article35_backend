from flask import Flask, Blueprint, request, g
from modles.user import User
from serializers.user import UserSchema, PopulateUserSchema
from securerouter.secure_route import secure_route
from marshmallow import ValidationError

user_schema = UserSchema()
populate_user = PopulateUserSchema()

router = Blueprint(__name__, 'users')

@router.route('/signup', methods=['POST'])
def signup():

    request_body = request.get_json()
    user = populate_user.load(request_body)
    user.save()
    return { 'message': 'Confirmed'}, 200

@router.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	user = User.query.filter_by(email=data['email']).first()

	if not user:
		return { 'message': 'Unauthorized User' }, 401

	if not user.validate_password(data['password']):
		return { 'message': 'Invalid Username or Password.' }, 402

	token = user.generate_token()
	
	return {'token': token, 'username': user.username, 'user_id': user.id, 'message': 'Welcome back!'}

@router.route('/users', methods=['GET'])
def user_index(id):
	users = user.query.all()
	return user_schema.jsonify(users, many=True), 200

@router.route('/users', methods=['GET'])
def user_index():