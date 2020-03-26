import datetime
import jwt

from .. import db, flask_bcrypt
from app.main.model.blacklist import BlacklistToken
from ..config import key


# db.Model 상속 for sqlalchemy
class User(db.Model):
    """User Model : 사용자 정보"""
    __tablename__ = "user"

    # 테이블 컬럼 정의
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property  # getter
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter  # Setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """패스워드 비교"""
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        인증토큰 생성
        :param user_id: 
        :return: string 
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload
                , key
                , algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        인증토큰 검증
        :param auth_token: 
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms='HS256', verify=True)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return '인증 토큰, 재로그인 필요'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return '인증만료, 재로그인 필요'
        except jwt.InvalidTokenError:
            return '유효하지 않은 인증, 재로그인 필요'
