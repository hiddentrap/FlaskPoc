# Data Transfer Object

from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='사용자 관리')
    # for marshaling (obj -> json) for IDS API calls
    user = api.model('user', {
        'email': fields.String(required=True, description='메일주소')
        , 'username': fields.String(required=True, description='사용자명')
        , 'password': fields.String(required=True, description='패스워드')
        , 'public_id': fields.String(description='사용자 ID')
    })


class AuthDto:
    api = Namespace('auth', description='인증 관리')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='이메일 주소')
        , 'password': fields.String(required=True, description='The user password')
    })
