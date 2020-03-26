from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """사용자 로그인"""

    @api.doc('사용자 로그인')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)

@api.route('/logout')
class LogoutAPI(Resource):
    """사용자 로그아웃"""
    @api.doc('사용자 로그아웃')
    def post(self):
        # 인증헤더에서 인증토큰 가져오기
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
