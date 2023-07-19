# import json
# import unittest
# from website.utils.utils import db
# from website import create_app
# from .. import create_app
# from website.config.config import config_dict
# from website.models.auth import User, ApiKey




# class UserTestCase(unittest.TestCase):
    
#     def setUp(self):
#         self.app = create_app(config=config_dict['test'])
#         self.appctx = self.app.app_context() # Creates the db

#         self.appctx.push()
#         self.client = self.app.test_client()

#         db.create_all()


#     def tearDown(self): # teardown resets existing tables in the database
#         db.drop_all()

#         self.appctx.pop()

#         self.app = None

#         self.client = None

#     def test_user_registration(self):
        
#         data = {
#             "username": "testuser",
#             "email": "testuser@gmail.com",
#             "password": "password"
#         }
#         response = self.client.post('/auth/signup', json=data)

#         user = User.query.filter_by(email="testuser@gmail.com").first()
        
#         assert user.username == "testuser"

#         assert response.status_code == 201


#     def test_user_login(self):
#         data = {
#             "email": "testuser@gmail.com",
#             "username": "testuser",
#             "password": "password"
#         }

#         self.client.post('/auth/signup', json=data)

#         login_data = {
#             "email": "testuser@gmail.com",
#             "password": "password"
#         }

#         response = self.client.post('/auth/login', json=login_data)

#         assert response.status_code == 202

    

    

























# # class UserTest(unittest.TestCase):
# #     def setUp(self):
# #         self.app = create_app(config=config_dict['test'])
# #         self.appcontext = self.app.app_context # creates the test client 

# #         self.appcontext.push() # pushes the app context to the test client
# #         self.client = self.app.test_client() # creates the test client

# #         db.create_all() # creates all the tables in the database


# #     def tearDown(self):
# #         db.drop_all() # drops all the tables in the database
# #         self.appcontext.pop() # pops the app context from the test client
# #         self.app = None # sets the app to None
# #         self.client = None # sets the client to None

# #     def test_user_registration(self):
# #         """
# #             Test User Registration
# #         """

# #         data = {
# #             'username': 'testuser',
# #             'email': 'testuser@gmail.com',
# #             'password': 'testpassword'
# #         }
# #         response = self.client.post('auth/signup', json=data)
# #         user = User.query.filter_by(email=data['email']).first()
# #         assert user.username == data['username']
# #         assert response.status_code == 201


# #     def test_user_login(self):
        
# #         data = {
# #             'email': 'testuser@gmail.com',
# #             'password': 'testpassword'
# #         }
# #         response = self.client.post('auth/login', json=data)    
# #         assert response.status_code == 202
