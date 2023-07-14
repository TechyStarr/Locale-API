from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db, cache, limiter
from website.models.auth import User
from http import HTTPStatus
from website.models.data import Region, State, Lga, load_dataset, PlaceOfInterest
from .serializers import serialized_state, serialized_lga, serialized_region
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .auth import validate_api_key


search_ns = Namespace('Query', description='Search operations')

search_params = search_ns.parser()
search_params.add_argument('region', type=str, required=False, help='Filter by region')
search_params.add_argument('state', type=str, required=False, help='Filter by state')
search_params.add_argument('lga', type=str, required=False, help='Filter by lga')

# search_params.add_argument('page', type=int, required=false, help='Page number')
# search_params.add_argument('limit', type=int, required=false, help='Page limit')
# search_params.add_argument('sort', type=str, required=false, help='Sort by')
# search_params.add_argument('keyword', type=str, required=false, help='Search keyword')

auto_complete_model = search_ns.model(
    'AutoComplete', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Name"),
    }
)



state_model = search_ns.model(
    'State', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Name"),
        'region': fields.String(required=True, description="Region"),
        'region_id': fields.String(required=True, description="Region ID"),
        'capital': fields.String(required=True, description="Capital"),
        'slogan': fields.String(required=True, description="Slogan"),
        'landmass': fields.String(required=True, description="Landmass"),
        'population': fields.String(required=True, description="Population"),
        'dialect': fields.String(required=True, description="Dialect"),
        'latitude': fields.String(required=True, description="Latitude"),
        'longitude': fields.String(required=True, description="Longitude"),
        'website': fields.String(required=True, description="Website"),
        'borders': fields.String(required=True, description="Borders"),
        'places_of_interest': fields.String(required=True, description="Known For"),
        'lgas': fields.String(required=True, description="Local Government Areas"),
    }
)

lga_model = search_ns.model(
    'lga', {
        'id': fields.String(required=True),
        'lga_name': fields.String(required=True, description="LGA Name"),
        'state_id': fields.String(required=True, description="state"),
        'landmass': fields.String(required=True, description="Landmass"),
        'borders': fields.String(required=True, description="Borders"),
    }
)

region_model= search_ns.model(
    'Region', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
        'states': fields.Nested((state_model), required=True, description="States"),
    }
)

place_of_interest_model = search_ns.model(
    'PlaceOfInterest', {
        'name': fields.String(required=True, description="Name"),
        'image': fields.String(required=True, description="Image"),
        'location': fields.String(required=True, description="Location"),
        'description': fields.String(required=True, description="Description")
    }
)

location_model = search_ns.model(
    'Location', {
        'name': fields.String(required=True, description="Location Name"),
        'region': fields.Nested(region_model),
        'state': fields.Nested(state_model),
        'lga': fields.Nested(lga_model),
    }
)


@search_ns.route('/')
class Query(Resource):
    @search_ns.doc('search_query')
    @search_ns.marshal_with(state_model, lga_model, region_model)
    @jwt_required(optional=True)
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self):
        """
        Search for states, regions and local government areas"""
        keyword = request.args.get('keyword')  # Get the search keyword from the query parameters
        # get_auto_complete(self, keyword)
        results = []
        if keyword:
            # Perform the search query based on the keyword
            results = State.query.join(Region).filter(
                db.or_(
                    Region.name.ilike(f'%{keyword}%'),  # Search by region name
                    State.slogan.ilike(f'%{keyword}%'),  # Search by state slogan
                    State.name.ilike(f'%{keyword}%'),  # Search by state name
                    State.capital.ilike(f'%{keyword}%'),  # Search by state capital
                    # Lga.lga_name.ilike(f'%{keyword}%'),  # Search by local government areas
                    # State.lgas.ilike(f'%{keyword}%')  # Search by local government areas
                )
            ).all()
            
            data = []

            # Serialize the regions
            data = ([serialized_region(region) for region in results])

            # Serialize the states
            data = ([serialized_state(state) for state in results])


            return results, 200
        else:
            return {'message': 'Enter a search keyword'}, 400


@search_ns.route('/filter')
class Filter(Resource):
    @search_ns.doc('filter_query')
    @search_ns.expect(search_params)
    @search_ns.marshal_with(state_model, lga_model, region_model)
    @jwt_required(optional=True)
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self):
        args = search_params.parse_args() 
        region = request.args.get('region')
        state = request.args.get('state')
        lga = request.args.get('lga')

        query = State.query.join(Region).join(Lga)

        if region:
            query = query.filter(Region.name.ilike(f'%{region}%'))
        if state:
            query = query.filter(State.name.ilike(f'%{state}%'))
        if lga:
            query = query.filter(Lga.lga_name.ilike(f'%{lga}%'))

        results = query.all()

        return results, 200
    

@search_ns.route('/places')
class RetrieveRegion(Resource):
    @search_ns.marshal_with(place_of_interest_model, as_list=True)
    @search_ns.doc(
        description='Get all Places of interest',
    )
    @jwt_required()
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self):
        """
            Get all places of interest
        """
        # places = PlaceOfInterest.query.limit(3).all()
        places = PlaceOfInterest.query.all()
        if places is None:
            return {'message': 'No Place found'}, HTTPStatus.NOT_FOUND

        return places, HTTPStatus.OK


@search_ns.route('/place/state/<int:state_id>')
class PlacesPerState(Resource):
    @search_ns.doc('regions_query')
    @search_ns.marshal_with(place_of_interest_model, as_list=True)
    @jwt_required(optional=True)
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self, state_id):
        """
            Get all places of interest in a state
        """
        state = State.query.get_or_404(state_id)
        if state:
            places = PlaceOfInterest.query.filter_by(state_id=state_id).all()
            return places, 200
        else:
            return {'message': 'No Place found'}, 404


@search_ns.route('/places')
class Places(Resource):
    @search_ns.doc('places_query')
    @search_ns.marshal_with(state_model, lga_model, region_model)
    @jwt_required(optional=True)
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self):
        """
            Search for places of interest
        """
        keyword = request.args.get('keyword')
        if keyword:
            results = PlaceOfInterest.query.filter(
                db.or_(
                    PlaceOfInterest.name.ilike(f'%{keyword}%'),  # Search by places of interest
                    PlaceOfInterest.description.ilike(f'%{keyword}%'),  # Search by places of interest description
                    PlaceOfInterest.location.ilike(f'%{keyword}%'),  # Search by places of interest location
                )
            ).all()
            return results, 200
        else:
            return {'message': 'Enter a search keyword'}, 400
    

# route for filtering
# /api/locations?region=<region_name>&state=<state_name>&lga=<lga_name>
# http://127.0.0.1:5000/query/filter?region=South&state=Abia&lga=Umuahia%20North