from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db
from website.models.users import User
from http import HTTPStatus
from website.models.data import Region, State, Lga, load_dataset
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..api.users import validate_api_key

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
        'id': fields.String(required=True),
        'lga_name': fields.String(required=True, description="LGA Name"),
        'state_id': fields.String(required=True, description="state"),
        'landmass': fields.String(required=True, description="Landmass"),
        'borders': fields.String(required=True, description="Borders"),
    }
)




state_model = view_namespace.model(
    'State', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
        'region': fields.String(required=True, description="Region"),
        'region_id': fields.String(required=True, description="Region ID"),
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
        'places_of_interest': fields.String(description="Top Places of Interest"),
    }
)



region_model= view_namespace.model(
    'Region', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
        'state': fields.Nested((state_model), required=True, description="States"),
    }
)


@view_namespace.route('/load-dataset')
class LoadDatasetResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    def post(self):
        if Region.query.first() or State.query.first() or Lga.query.first():
            abort (400, 'Dataset already loaded')
        load_dataset()
        return {'message': 'Dataset loaded successfully'}
    

@view_namespace.route('/read-dataset')
class readData(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    def get(self):
        # load_dataset()
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
        regions = Region.query.all()
        if regions is None:
            abort(404, 'No Region found')
        try:
            return regions, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@view_namespace.route('/create')
class CreateRegions(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.expect(region_model)
    @view_namespace.marshal_with(region_model)
    @view_namespace.doc(
        description='Create a new Region',
    )
    @jwt_required()
    def post(self):
        data = view_namespace.payload
        region = Region.query.filter_by(name=data['name']).first()
        if region:
            abort(400, 'Region already exists')
        region = Region(
            name=data['name']
        )  
        try:
            region.save()
            response = {region: region, 'message': 'Region created successfully'}
            return response, HTTPStatus.CREATED
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@view_namespace.route('/update-region/<string:region_id>')
class UpdateRegion(Resource): 
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)
    @view_namespace.marshal_with(region_model)
    @view_namespace.doc(
        description='Get a Region by ID',
    )
    @jwt_required()
    def patch(self, region_id):
        region = Region.query.filter_by(id=region_id).first()
        if not region:
            abort(404, 'Region not found')
        try:
            return region, HTTPStatus.OK
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
        lga = Lga.query.all()
        if lga is None:
            abort(404, 'No LGA found')
        try:
            return lga, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR



@view_namespace.route('/lgas/<string:lga_id>')
class Retrieve(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

    @view_namespace.marshal_with(lga_model)
    @view_namespace.doc(
        description='Get a LGA by ID',
    )
    @jwt_required()
    def get(self, lga_id):
        lga = Lga.query.filter_by(id=lga_id).first()
        if lga is None:
            abort(404, 'LGA not found')
        try:
            return lga, HTTPStatus.FOUND
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


    def patch(self, lga_id):
        data = view_namespace.payload
        lga = Lga.query.filter_by(id=lga_id).first()
        if not lga:
            abort(404, 'LGA not found')
        try:
            lga.name = data['name']
            lga.state_id = data['state_id']
            return lga, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
