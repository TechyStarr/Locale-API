from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db
from website.models.auth import User
from http import HTTPStatus
from website.models.data import Region, State, Lga, load_dataset, PlaceOfInterest
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .auth import validate_api_key

app = Flask(__name__)

# cache response for 60 seconds
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# rate limit of 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )




view_namespace = Namespace('View', description = 'View related operations')

lga_model = view_namespace.model(
    'lga', {
        # 'id': fields.String(required=True),
        'lga_name': fields.String(required=True, description="LGA Name"),
        'state_id': fields.String(required=True, description="state"),
        'landmass': fields.String(required=True, description="Landmass"),
        'borders': fields.String(required=True, description="Borders"),
    }
)

place_model = view_namespace.model('Place', {
    'name': fields.String(required=True),
    'location': fields.String(required=True),
    'image': fields.String(required=True),
    'description': fields.String(required=True),
    }
)


state_model = view_namespace.model(
    'State', {
        # 'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
        'region': fields.String(required=True, description="Region"),
        # 'region_id': fields.String(required=True, description="Region ID"),
        'capital': fields.String(required=True, description="Capital"),
        'slogan': fields.String(required=True, description="Slogan"),
        'lgas': fields.Nested((lga_model), description="Local Government Areas"),
        'landmass': fields.String(required=True, description="Landmass"),
        'population': fields.String(required=True, description="Population"),
        'dialect': fields.String(required=True, description="Dialect"),
        'latitude': fields.String(required=True, description="Latitude"),
        'longitude': fields.String(required=True, description="Longitude"),
        'website': fields.String(required=True, description="Website"),
        'borders': fields.String(required=True, description="Borders"),
        'places_of_interest': fields.Nested((place_model), description="Places of Interest"),
    }
)



region_model= view_namespace.model(
    'Region', {
        # 'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
        'state': fields.Nested((state_model), required=True, description="States"),
    }
)


@view_namespace.route('/load-dataset')
class LoadDatasetResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    def post(self):
        """
            Manually Load dataset
        """
        if Region.query.first() or State.query.first() or Lga.query.first():
            abort (400, 'Dataset already loaded')
        load_dataset()
        return {'message': 'Dataset loaded successfully'}
    


@view_namespace.route('/read-dataset')
class readData(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    def get(self):
        """
            Read dataset
        """
        f = open('website/models/dataset.json', 'r', encoding='utf-8')
        print(f.read())
        return {'message': 'Dataset loaded successfully'}
    




# Regions
@view_namespace.route('/regions')
class RetrieveRegion(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)
    @view_namespace.marshal_with(region_model, as_list=True)
    @view_namespace.doc(
        description='Get all Regions',
    )
    @jwt_required()
    def get(self):
        """
            Get all Regions with their States metadata 
        """
        regions = Region.query.all()
        if regions is None:
            abort(404, 'No Region found')
        try:
            return regions, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR




# retrieve data under a region
@view_namespace.route('/regions/<string:region_id>/states')
class RetrieveStatesUnderRegion(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(state_model, as_list=True)
    @view_namespace.doc(
        description='Get all States under a Region',
    )
    @jwt_required()
    def get(self, region_id):
        """
            Get all States under a Region
        """
        states = State.query.filter_by(region_id=region_id).all()
        if states is None:
            return {'message': 'No State found'}, HTTPStatus.NOT_FOUND

        try:
            return states, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR





# States
@view_namespace.route('/states')
class SearchResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(state_model, as_list=True)
    @view_namespace.doc(
        description='Get all States',
    )
    @jwt_required()
    def get(self):
        """
            Get all States
        """
        states = State.query.all()
        if states is None:
            abort(404, 'No State found')
        try:
            return states, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR



# LGA
@view_namespace.route('/lgas')
class RetrieveResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(lga_model, as_list=True)
    @view_namespace.doc(
        description='Get all lgas',
    )
    @jwt_required()
    def get(self):
        """
            Get all lgas
        """
        lga = Lga.query.all()
        if lga is None:
            abort(404, 'No LGA found')
        try:
            return lga, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR



@view_namespace.route('/state/<string:state_id>')
class RetrieveState(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(state_model)
    @view_namespace.doc(
        description='Get a state by ID',
    )
    @jwt_required()
    def get(self, state_id):
        """
            Get a state by ID
        """
        state = State.query.filter_by(id=state_id).first()
        if state is None:
            abort(404, 'State not found')
        try:
            return state, HTTPStatus.FOUND
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR



@view_namespace.route('/lga/<string:lga_id>')
class RetrieveLGA(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(lga_model)
    @view_namespace.doc(
        description='Get a LGA by ID',
    )
    @jwt_required()
    def get(self, lga_id):
        """
            Get a LGA by ID
        """
        lga = Lga.query.filter_by(id=lga_id).first()
        if lga is None:
            abort(404, 'LGA not found')
        try:
            return lga, HTTPStatus.FOUND
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR



@view_namespace.route('/places')
class RetrievePlaces(Resource):
    @view_namespace.marshal_with(place_model, as_list=True)
    @view_namespace.doc(
        description='Get all places',
    )
    @jwt_required()
    def get(self):
        """
            Get all places of interest
        """
        places = PlaceOfInterest.query.all()
        if places is None:
            abort(404, 'No Place found')
        try:
            return places, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

