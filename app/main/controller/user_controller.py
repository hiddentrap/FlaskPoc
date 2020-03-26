from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user


@api.route('/')  # 리소스 라우팅
class UserList(Resource):  # flask-restplus Resource 추상 클래스 상속
    """정의하지 않은 HTTP메서드로 호출시 405 Method Not Allowed 리턴"""

    @api.doc('사용자 목록 조회')  # api 설명
    @api.marshal_list_with(_user, envelope='data')  # obj -> json
    def get(self):
        """등록된 모든 사용자 목록"""
        return get_all_users()

    @api.response(201, '사용자 등록 성공')
    @api.doc('사용자 등록')
    @api.expect(_user, validate=True)  # 예상 input model
    def post(self):
        """신규 사용자 등록"""
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', '사용자 아이디')  # 예상 파라메터
@api.response(404, '사용자가 조회 실패')
class User(Resource):
    @api.doc('사용자 조회')
    @api.marshal_list_with(_user)
    def get(self, public_id):
        """사용자 아이디로 사용자 조회"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
