import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.utils.util import encode_token
from faker import Faker
from app.models import Role, Post, Comment
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    @patch('app.routes.db.session.get')
    def test_get_all_users(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
        # Mock the user and set role to admin
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user
        
        # Ensure that get returns the correct user (to set role correctly)
        mock_get.return_value = mock_user
        
        # Mock the query to return a list of users
        mock_user2 = MagicMock()
        mock_user2.user_id = 2
        mock_user_list = [mock_user, mock_user2]
        
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = mock_user_list
        mock_execute.return_value = mock_query

        # Generate a token and perform the request
        token = encode_token(mock_user.user_id)
        response = self.client.get('/users', headers={'Authorization': f'Bearer {token}'})
        
        # Assert the status code and content
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('user_id', response.json[0])

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
    @patch('app.routes.db.session.get')
    def test_create_post(self, mock_get, mock_commit, mock_add, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

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
    @patch('app.routes.db.session.get')
    def test_get_all_posts(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
        logger.debug("Starting test_get_all_posts")

        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user
        mock_get.return_value = mock_user

        mock_post = Post(post_id=1, title="Test Title", body="Test Content")
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_post]
        logger.debug(f"Mock execute return value: {mock_query.scalars().all()}")
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        logger.debug(f"Generated token: {token}")
        response = self.client.get('/posts', headers={'Authorization': f'Bearer {token}'})
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response data: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('post_id', response.json[0])
        self.assertIn('title', response.json[0])
        self.assertIn('body', response.json[0])



    # @patch('app.auth.token_auth.verify_token')
    # @patch('app.auth.token_auth.current_user')
    # @patch('app.routes.db.session.execute')
    # @patch('app.routes.db.session.get')
    # def test_get_all_posts(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
    #     mock_user = MagicMock()
    #     mock_user.user_id = 1
    #     mock_user.role = MagicMock()
    #     mock_user.role.role_name = 'admin'
    #     mock_current_user.return_value = mock_user
    #     mock_verify_token.return_value = mock_user

    #     mock_get.return_value = mock_user

    #     mock_post = MagicMock()
    #     mock_post.post_id = 1
    #     mock_query = MagicMock()
    #     mock_query.scalars().all.return_value = [mock_post]
    #     mock_execute.return_value = mock_query

    #     token = encode_token(mock_user.user_id)
    #     response = self.client.get('/posts', headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)
    #     self.assertGreater(len(response.json), 0)
    #     self.assertIn('post_id', response.json[0])

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
    @patch('app.routes.db.session.get')
    def test_create_comment(self, mock_get, mock_commit, mock_add, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

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
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_comment.user_id = mock_user.user_id
        mock_get.return_value = mock_comment

        mock_get.return_value = mock_user # Sets the admin role for the user

        token = encode_token(mock_user.user_id)
        response = self.client.delete('/comments/1', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    @patch('app.auth.token_auth.verify_token')
    @patch('app.auth.token_auth.current_user')
    @patch('app.routes.db.session.execute')
    @patch('app.routes.db.session.get')
    def test_get_all_comments(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user

        mock_get.return_value = mock_user

        mock_comment = MagicMock()
        mock_comment.comment_id = 1
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_comment]
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        response = self.client.get('/comments', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('comment_id', response.json[0])

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
    @patch('app.routes.db.session.get')
    def test_list_comments_for_post(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
        logger.debug("Starting test_list_comments_for_post")

        mock_user = MagicMock()
        mock_user.user_id = 1
        mock_user.role = MagicMock()
        mock_user.role.role_name = 'admin'
        mock_current_user.return_value = mock_user
        mock_verify_token.return_value = mock_user
        mock_get.return_value = mock_user

        mock_comment = Comment(comment_id=1, post_id=1, content="Test content for post")
        mock_query = MagicMock()
        mock_query.scalars().all.return_value = [mock_comment]
        logger.debug(f"Mock execute return value: {mock_query.scalars().all()}")
        mock_execute.return_value = mock_query

        token = encode_token(mock_user.user_id)
        logger.debug(f"Generated token: {token}")
        response = self.client.get('/posts/1/comments', headers={'Authorization': f'Bearer {token}'})
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response data: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('comment_id', response.json[0])
        self.assertIn('post_id', response.json[0])
        self.assertIn('content', response.json[0])




    # @patch('app.auth.token_auth.verify_token')
    # @patch('app.auth.token_auth.current_user')
    # @patch('app.routes.db.session.execute')
    # @patch('app.routes.db.session.get')
    # def test_list_comments_for_post(self, mock_get, mock_execute, mock_current_user, mock_verify_token):
    #     mock_user = MagicMock()
    #     mock_user.user_id = 1
    #     mock_user.role = MagicMock()
    #     mock_user.role.role_name = 'admin'
    #     mock_current_user.return_value = mock_user
    #     mock_verify_token.return_value = mock_user

    #     mock_get.return_value = mock_user

    #     mock_comment = MagicMock()
    #     mock_comment.comment_id = 1
    #     mock_comment.post_id = 1
    #     mock_comment.content = fake.sentence()
    #     mock_comment.user_id = mock_user.user_id

    #     mock_query = MagicMock()
    #     mock_query.scalars().all.return_value = [mock_comment]
    #     mock_execute.return_value = mock_query

    #     token = encode_token(mock_user.user_id)
    #     response = self.client.get('/posts/1/comments', headers={'Authorization': f'Bearer {token}'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)
    #     self.assertGreater(len(response.json), 0)
    #     self.assertIn('comment_id', response.json[0])
    #     self.assertIn('content', response.json[0])
    #     self.assertIn('user_id', response.json[0])
    #     self.assertIn('post_id', response.json[0])


if __name__ == '__main__':
    unittest.main()


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