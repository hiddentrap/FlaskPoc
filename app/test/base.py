from flask_testing import TestCase
from app.main import db
from manage import app


class BaseTestCase(TestCase):
    """ 상속받는 테스트 케이스의 테스트 환경 초기화 """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
