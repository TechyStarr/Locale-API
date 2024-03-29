import json
import unittest
from website.utils.utils import db
from website import create_app
from .. import create_app
from flask_jwt_extended import create_access_token
from website.config.config import config_dict
from website.models.data import Region, State, Lga, load_dataset

class TestRetrieveRegion(unittest.TestCase):

    
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context() # Creates the db

        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self): # teardown resets existing tables in the database
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_get_regions(self):
        with self.app.test_client() as client:

            sign_up_data = {
            "email": "testuser@gmail.com",
            "username": "testuser",
            "password": "password"
            }

            self.client.post('/auth/signup', json=sign_up_data)

            token = create_access_token(identity="testuser")

            headers = {
            "Authorization": f"Bearer {token}"
            }

            region_data = {
                "name": "South East",
                "states": [
                    {
                        "name": "Abia State",
                        "lgas": [
                            {
                                "lga_name": "Aba North"
                            },
                            {
                                "lga_name": "Aba South"
                            }
                        ]
                    },
                    {
                        "name": "Anambra State",
                        "lgas": [
                            {
                                "lga_name": "Aguata"
                            },
                            {
                                "lga_name": "Anambra East"
                            }
                        ]
                    }
                ]
            }
        

            response = self.client.get('/views/regions', headers=headers, json=region_data)

            assert response.status_code == 200
        


    def test_get_states(self):
        with self.app.test_client() as client:

            sign_up_data = {
            "email": "testuser@gmail.com",
            "username": "testuser",
            "password": "password"
            }

            self.client.post('/auth/signup', json=sign_up_data)

            token = create_access_token(identity="testuser")

            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = self.client.get('/views/states')

            states = State.query.all()
            # assert response.status_code == 200

            assert len(states) == 37 # 36 states + FCT

            assert states[0].name == "Abia State"
            assert states[1].name == "Adamawa State"

    def test_get_lgas(self):
        with self.app.test_client() as client:

            sign_up_data = {
            "email": "testuser@gmail.com",
            "username": "testuser",
            "password": "password"
            }

            self.client.post('/auth/signup', json=sign_up_data)

            token = create_access_token(identity="testuser")

            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = self.client.get('/views/lgas')

            lgas = Lga.query.all()
            # assert response.status_code == 200

            assert len(lgas) == 27

            assert lgas[0].lga_name == "Aba North"
            assert lgas[1].lga_name == "Aba South"


    def test_get_states_under_region(self):
        # with self.app.test_client() as client:

        sign_up_data = {
        "email": "testuser@gmail.com",
        "username": "testuser",
        "password": "password"
        }

        self.client.post('/auth/signup', json=sign_up_data)

        token = create_access_token(identity="testuser")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        test_region = Region(name="South East")
        db.session.add(test_region)
        db.session.commit()

        region_id = test_region.id

        response = self.client.get('/views/regions/1/states')
        assert response.status_code == 200

        states = State.query.filter_by(region_id=region_id).all()

        # assert len(states) == 37 # 36 states + FCT

        assert states[0].name == "Abia State"
        assert states[1].name == "Anambra State"



            

    def test_get_regions_unauthorized(self):
        with self.app.test_client() as client:

            response = self.client.get('/views/regions')

            # assert response.status_code == 401
