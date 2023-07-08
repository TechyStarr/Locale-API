# import json
# import pytest
# # from website import create_app
# # from .. import create_app
# # from website.config.config import config_dict
# # from website.models.users import User, ApiKey

# from website.models.users import User, ApiKey

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     client = app.test_client()
#     yield client

# def test_login(client):
#     data  = {
#         'email': 'test@example.com',
#         'password': 'test'
#     }
#     response = client.post('/api/v1/auth/login', data=json.dumps(data), content_type='application/json')
#     assert response.status_code == 200