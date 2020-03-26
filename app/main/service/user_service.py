import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()  # 중복체크
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4())
            , email=data['email']
            , username=data['username']
            , password=data['password']
            , registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
    #     response_object = {
    #         'status': 'success'
    #         , 'message': 'Successfully registered.'
    #     }
    #     return response_object, 201  # Json 변환은 Flask-restpuls가 자동으로 수행
        return generate_token(new_user) # 로그인 인증 토큰 발급
    else:
        response_object = {
            'status': 'fail'
            , 'message': 'User already exists. Please Log in.'
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # 인증토큰 생성
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success'
            , 'message': 'Successfully registered.'
            , 'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail'
            , 'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
