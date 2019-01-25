from flask import jsonify
from app.exceptions import ValidationError
from . import api_1_0

def bad_request(message):
	 response = jsonify({'error': 'bad request', 'message': message})
	 reposnse.status_code = 400
	 return response


def unauthorized(message):
	response = jsonify({'error': 'unauthorized', 'message': message})
	reposnse.status_code = 401
	return response


def forbidden(message):
	response = jsonify({'error': 'forbidden', 'message': message})
	response.status_code = 403
	return response

@api_1_0.errorhandler(ValidationError)
def validation_error(e):
	return bad_request(e.args[0])