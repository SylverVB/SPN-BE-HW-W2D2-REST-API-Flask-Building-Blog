# import unittest
# from unittest.mock import patch, MagicMock
# from app import app
# from app.utils.util import encode_token
# from faker import Faker
# from app.models import Role
# # import logging
# # import sys

# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# fake = Faker()

# class TestTokenEndpoint(unittest.TestCase):
#     def setUp(self):
#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     @patch('app.routes.encode_token')
#     @patch('app.routes.db.session.scalars')
#     @patch('app.routes.check_password_hash')
#     def test_successful_authenticate(self, mock_check_hash, mock_scalars, mock_encode_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_query = MagicMock()
#         mock_query.first.return_value = mock_user
#         mock_scalars.return_value = mock_query

#         mock_check_hash.return_value = True
#         mock_encode_token.return_value = 'random.jwt.token'

#         request_body = {
#             "username": fake.user_name(),
#             "password": fake.password()
#         }

#         response = self.client.post('/token', json=request_body)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['token'], 'random.jwt.token')

#     @patch('app.routes.db.session.scalars')
#     def test_unauthorized_user(self, mock_scalars):
#         mock_query = MagicMock()
#         mock_query.first.return_value = None
#         mock_scalars.return_value = mock_query

#         request_body = {
#             "username": fake.user_name(),
#             "password": fake.password()
#         }

#         response = self.client.post('/token', json=request_body)

#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(response.json['error'], 'Username and/or password is incorrect')


# class TestUserEndpoints(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()
    
#     @patch('app.routes.db.session.add')
#     @patch('app.routes.db.session.commit')
#     @patch('app.routes.db.session.execute')
#     @patch('app.routes.db.session.scalars')
#     def test_create_user(self, mock_scalars, mock_execute, mock_commit, mock_add):
#         # Simulate no existing users with the same username or email
#         mock_query = MagicMock()
#         mock_query.all.return_value = []
#         mock_scalars.return_value = mock_query
        
#         # Simulate fetching the role from the database
#         mock_role = Role(role_id=1, role_name='admin')
#         mock_execute.return_value.scalar_one_or_none.return_value = mock_role

#         request_body = {
#             "first_name": fake.first_name(),
#             "last_name": fake.last_name(),
#             "role": "admin",
#             "username": fake.user_name(),
#             "email": fake.email(),
#             "password": fake.password()
#         }

#         response = self.client.post('/users', json=request_body)

#         self.assertEqual(response.status_code, 201)
#         self.assertIn("user_id", response.json)
#         self.assertEqual(response.json['first_name'], request_body['first_name'])
#         self.assertEqual(response.json['last_name'], request_body['last_name'])
#         self.assertEqual(response.json['username'], request_body['username'])
#         self.assertEqual(response.json['email'], request_body['email'])
    
#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_delete_user(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_user.role.role_name = 'admin'
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_get.return_value = mock_user

#         token = encode_token(mock_user.user_id)
#         response = self.client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.execute')
#     def test_get_all_users(self, mock_execute, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_user.role.role_name = 'admin'
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user
        
#         # mock_get.return_value = mock_user

#         mock_query = MagicMock()
#         mock_query.scalars().all.return_value = [mock_user]
#         mock_execute.return_value = mock_query

#         token = encode_token(mock_user.user_id)
#         # logger.info(f"Token: {token}")
#         response = self.client.get('/users', headers={'Authorization': f'Bearer {token}'})
#         # logger.info(f"Response status code: {response.status_code}")
#         # if response.status_code != 200:
#             # logger.error(f"Error response data: {response.data}")
#         self.assertEqual(response.status_code, 200)


#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     def test_get_single_user(self, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_user.role.role_name = 'admin'
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_get.return_value = mock_user

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/users/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_update_user(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_user.role.role_name = 'admin'
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_get.return_value = mock_user

#         request_body = {
#             "first_name": fake.first_name(),
#             "last_name": fake.last_name(),
#             "email": fake.email()
#         }

#         token = encode_token(mock_user.user_id)
#         response = self.client.put('/users/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)


# class TestPostEndpoints(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.add')
#     @patch('app.routes.db.session.commit')
#     def test_create_post(self, mock_commit, mock_add, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         request_body = {
#             "title": fake.sentence(),
#             "body": fake.text(),
#         }

#         token = encode_token(mock_user.user_id)
#         # logger = logging.getLogger(__name__)
#         # logger.info(f"Token for test: {token}")
#         response = self.client.post('/posts', json=request_body, headers={'Authorization': f'Bearer {token}'})
#         # logger.info(f"Response status code: {response.status_code}")
#         # logger.info(f"Response data: {response.data}")
#         self.assertEqual(response.status_code, 201)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_delete_post(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_post = MagicMock()
#         mock_post.post_id = 1
#         mock_post.user_id = mock_user.user_id
#         mock_get.return_value = mock_post

#         token = encode_token(mock_user.user_id)
#         response = self.client.delete('/posts/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.execute')
#     def test_get_all_posts(self, mock_execute, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_post = MagicMock()
#         mock_post.post_id = 1
#         mock_query = MagicMock()
#         mock_query.scalars().all.return_value = [mock_post]
#         mock_execute.return_value = mock_query

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/posts', headers={'Authorization': f'Bearer {token}'})
#         # logger.info(f"Token: {token}")
#         # logger.info(f"Response status code: {response.status_code}")
#         # logger.info(f"Response data: {response.data}")
#         # sys.stdout.flush()
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     def test_get_single_post(self, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_post = MagicMock()
#         mock_post.post_id = 1
#         mock_get.return_value = mock_post

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/posts/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_update_post(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_post = MagicMock()
#         mock_post.post_id = 1
#         mock_post.user_id = mock_user.user_id
#         mock_get.return_value = mock_post

#         request_body = {
#             "title": fake.sentence(),
#             "body": fake.text()
#         }

#         token = encode_token(mock_user.user_id)
#         response = self.client.put('/posts/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)


# class TestCommentEndpoints(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.add')
#     @patch('app.routes.db.session.commit')
#     def test_create_comment(self, mock_commit, mock_add, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         request_body = {
#             "content": fake.text(),
#             "post_id": 1,
#         }

#         token = encode_token(mock_user.user_id)
#         response = self.client.post('/comments', json=request_body, headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 201)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_delete_comment(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_user.role.role_name = 'admin'
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_comment = MagicMock()
#         mock_comment.comment_id = 1
#         mock_comment.user_id = mock_user.user_id
#         mock_get.return_value = mock_comment

#         mock_get.return_value = mock_user # sets the admin role for the user

#         token = encode_token(mock_user.user_id)
#         response = self.client.delete('/comments/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.execute')
#     def test_get_all_comments(self, mock_execute, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_comment = MagicMock()
#         mock_comment.comment_id = 1
#         mock_query = MagicMock()
#         mock_query.scalars().all.return_value = [mock_comment]
#         mock_execute.return_value = mock_query

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/comments', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     def test_get_single_comment(self, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_comment = MagicMock()
#         mock_comment.comment_id = 1
#         mock_get.return_value = mock_comment

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/comments/1', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.execute')
#     def test_list_comments(self, mock_execute, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_comment = MagicMock()
#         mock_comment.comment_id = 1
#         mock_comment.post_id = 1
#         mock_comment.content = fake.sentence()
#         mock_comment.user_id = mock_user.user_id

#         mock_query = MagicMock()
#         mock_query.scalars().all.return_value = [mock_comment]
#         mock_execute.return_value = mock_query

#         token = encode_token(mock_user.user_id)
#         response = self.client.get('/comments', headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(response.json, list)
#         self.assertGreater(len(response.json), 0)
#         self.assertIn('comment_id', response.json[0])
#         self.assertIn('content', response.json[0])
#         self.assertIn('user_id', response.json[0])
#         self.assertIn('post_id', response.json[0])

#     @patch('app.auth.token_auth.verify_token')
#     @patch('app.auth.token_auth.current_user')
#     @patch('app.routes.db.session.get')
#     @patch('app.routes.db.session.commit')
#     def test_update_comment(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
#         mock_user = MagicMock()
#         mock_user.user_id = 1
#         mock_current_user.return_value = mock_user
#         mock_verify_token.return_value = mock_user

#         mock_comment = MagicMock()
#         mock_comment.comment_id = 1
#         mock_comment.user_id = mock_user.user_id
#         mock_get.return_value = mock_comment

#         request_body = {
#             "content": fake.text(),
#             "post_id": 1
#         }

#         token = encode_token(mock_user.user_id)
#         response = self.client.put('/comments/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(response.status_code, 200)

# # # if __name__ == '__main__':
# # #     unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.utils.util import encode_token
from faker import Faker
from app.models import Role

fake = Faker()

class TestTokenEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('app.routes.encode_token')
    @patch('app.routes.db.session.scalars')
    @patch('app.routes.check_password_hash')
    def test_successful_authenticate(self, mock_check_hash, mock_scalars, mock_encode_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_query = MagicMock()
        mock_query.first.return_value = mock_user
        mock_scalars.return_value = mock_query

        mock_check_hash.return_value = True
        mock_encode_token.return_value = 'random.jwt.token'

        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['token'], 'random.jwt.token')

    @patch('app.routes.db.session.scalars')
    def test_unauthorized_user(self, mock_scalars):
        mock_query = MagicMock()
        mock_query.first.return_value = None
        mock_scalars.return_value = mock_query

        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Username and/or password is incorrect')


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    @patch('app.routes.db.session.execute')
    @patch('app.routes.db.session.scalars')
    def test_create_user(self, mock_scalars, mock_execute, mock_commit, mock_add):
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_scalars.return_value = mock_query
        
        mock_role = Role(role_id=1, role_name='admin')
        mock_execute.return_value.scalar_one_or_none.return_value = mock_role

        request_body = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "role": "admin",
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password()
        }

        response = self.client.post('/users', json=request_body)

        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json)
        self.assertEqual(response.json['first_name'], request_body['first_name'])
        self.assertEqual(response.json['last_name'], request_body['last_name'])
        self.assertEqual(response.json['username'], request_body['username'])
        self.assertEqual(response.json['email'], request_body['email'])
    
    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_delete_user(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

        token = encode_token(mock_user.user_id)
        response = self.client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.execute')
    def test_get_all_users(self, mock_execute, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user
        
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_user]
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        response = self.client.get('/users', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    def test_get_single_user(self, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

        token = encode_token(mock_user.user_id)
        response = self.client.get('/users/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_update_user(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

        request_body = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email()
        }

        token = encode_token(mock_user.user_id)
        response = self.client.put('/users/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)


class TestPostEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    def test_create_post(self, mock_commit, mock_add, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        request_body = {
            "title": fake.sentence(),
            "body": fake.text(),
        }

        token = encode_token(mock_user.user_id)
        response = self.client.post('/posts', json=request_body, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_delete_post(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_post = MagicMock()
        mock_post.post_id = 1
        mock_post.user_id = mock_user.user_id
        mock_get.return_value = mock_post

        token = encode_token(mock_user.user_id)
        response = self.client.delete('/posts/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.execute')
    def test_get_all_posts(self, mock_execute, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_post = MagicMock()
        mock_post.post_id = 1
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_post]
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        response = self.client.get('/posts', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    def test_get_single_post(self, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_post = MagicMock()
        mock_post.post_id = 1
        mock_get.return_value = mock_post

        token = encode_token(mock_user.user_id)
        response = self.client.get('/posts/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_update_post(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_post = MagicMock()
        mock_post.post_id = 1
        mock_post.user_id = mock_user.user_id
        mock_get.return_value = mock_post

        request_body = {
            "title": fake.sentence(),
            "body": fake.text()
        }

        token = encode_token(mock_user.user_id)
        response = self.client.put('/posts/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        mock_commit.assert_called_once()



class TestCommentEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    def test_create_comment(self, mock_commit, mock_add, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        request_body = {
            "content": fake.text(),
            "post_id": 1,
        }

        token = encode_token(mock_user.user_id)
        response = self.client.post('/comments', json=request_body, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_delete_comment(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()  # Adding this line
        mock_user.role.role_name = 'admin'  # Adding this line
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_comment.user_id = mock_user.user_id
        mock_get.return_value = mock_comment

        mock_get.return_value = mock_user # sets the admin role for the user

        token = encode_token(mock_user.user_id)
        response = self.client.delete('/comments/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.execute')
    def test_get_all_comments(self, mock_execute, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_comment]
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        response = self.client.get('/comments', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    def test_get_single_comment(self, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_get.return_value = mock_comment

        token = encode_token(mock_user.user_id)
        response = self.client.get('/comments/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.get')
    @patch('app.routes.db.session.commit')
    def test_update_comment(self, mock_commit, mock_get, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_comment.user_id = mock_user.user_id
        mock_get.return_value = mock_comment

        request_body = {
            "content": fake.text(),
            "post_id": 1
        }

        token = encode_token(mock_user.user_id)
        response = self.client.put('/comments/1', json=request_body, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)


    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.execute')
    def test_list_comments_for_post(self, mock_execute, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_comment.post_id = 1
        mock_comment.content = fake.sentence()
        mock_comment.user_id = mock_user.user_id

        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_comment]
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        response = self.client.get('/posts/1/comments', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('comment_id', response.json[0])
        self.assertIn('content', response.json[0])
        self.assertIn('user_id', response.json[0])
        self.assertIn('post_id', response.json[0])


if __name__ == '__main__':
    unittest.main()