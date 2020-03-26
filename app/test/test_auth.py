import unittest
import json
from app.test.base import BaseTestCase
from app.main.model.blacklist import BlacklistToken
from app.main import db


def register_user(self):
    return self.client.post(
        '/user/'
        , data=json.dumps(dict(
            email='example@gmail.com'
            , username='username'
            , password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login'
        , data=json.dumps(dict(
            email='example@gmail.com'
            , password='123456'
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_registered_user_login(self):
        """ 등록된 사용자 로그인"""
        with self.client:
            # 사용자 등록
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # 등록된 사용자 로그인
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

    def test_non_registered_user_login(self):
        """ 미등록 사용자 로그인 """
        with self.client:
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            print(data['message'])
            self.assertTrue(data['message'] == 'email or password does not match.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_valid_logout(self):
        """인증 토큰 만료전 로그아웃 검증"""
        with self.client:
            # 사용자 등록
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # 등록된 사용자 로그인
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

            # 유효한 인증 토큰 로그아웃
            response = self.client.post(
                '/auth/logout'
                , headers=dict(
                    Authorization='Bearer ' + json.loads(
                        login_response.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            resp_register = register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['Authorization'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = login_user(self)
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_login.data.decode())['Authorization'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == '인증 토큰, 재로그인 필요')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
