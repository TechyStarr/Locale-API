import json
import pytest
from website import create_app
from .. import create_app
from website.config.config import config_dict
from website.models.auth import User, ApiKey


@pytest.fixture(scope='module') # scope='module' means that the fixture is available to all tests in the module
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()
    yield test_client

def test_login(test_client):
    data = {
        'email': 'test@gmail.com',
        'password': 'test'
    }

    
    response = test_client.post('http://127.0.0.1:5000/auth/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in response.json
    access_token = response.json['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


