from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db

from website.models.users import User
from http import HTTPStatus
from website.models.data import Region, State, Lga, load_dataset, PlaceOfInterest
from .serializers import serialized_state, serialized_lga, serialized_region


search_ns = Namespace('Query', description='Search operations')

search_params = search_ns.parser()
search_params.add_argument('region', type=str, required=False, help='Filter by region')
search_params.add_argument('state', type=str, required=False, help='Filter by state')
search_params.add_argument('lga', type=str, required=False, help='Filter by lga')

# search_params.add_argument('page', type=int, required=false, help='Page number')
# search_params.add_argument('limit', type=int, required=false, help='Page limit')
# search_params.add_argument('sort', type=str, required=false, help='Sort by')
# search_params.add_argument('keyword', type=str, required=false, help='Search keyword')



state_model = search_ns.model(
    'State', {
        'id': fields.String(required=True),
        'name': fields.String(required=True, description="Course Name"),
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
        # 'No_of_LGAs': fields.String(required=True, description="No of LGAs"),
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

location_model = search_ns.model(
    'Location', {
        'name': fields.String(required=True, description="Location Name"),
        'region': fields.Nested(region_model),
        'state': fields.Nested(state_model),
        'lga': fields.Nested(lga_model),
    }
)



# @search_ns.route('/')
# class QueryStates(Resource):
#     @search_ns.doc('search_state')
#     # @search_ns.marshal_with(state_model, lga_model, region_model)

#     def get(self):

#         keyword = request.args.get('keyword')
#         if keyword:
#             # Perform the search query based on the keyword
#             results = State.query\
#             .join(Region)\
#             .join(Lga)\
#             .filter(
#                 db.or_(
#                     State.name.ilike(f'%{keyword}%'),
#                     State.capital.ilike(f'%{keyword}%'),
#                     # State.lgas.ilike(f'%{keyword}%'),
#                     Lga.lga_name.ilike(f'%{keyword}%'),
#                     Region.name.ilike(f'%{keyword}%')  # Include region name in the search
#                 )
#             ).all()
#             print(results)

#             # Serialize the search results
#             data = []
#             for state in results:
#                 serialized_state_data = serialized_state(state)
#                 serialized_region_data = serialized_region(state.region)
#                 serialized_lga_data = serialized_lga(state.lgas)
#                 data.append({
#                     'state': serialized_state_data,
#                     'region': serialized_region_data,
#                     'lga': serialized_lga_data
#                 })


#             return {'results': data}, 200

#         abort(HTTPStatus.BAD_REQUEST, 'No search keyword provided')










@search_ns.route('/')
class QueryStates(Resource):
    @search_ns.doc('search_query')
    @search_ns.marshal_with(state_model, lga_model, region_model)

    def post(self):

        keyword = request.args.get('keyword')  # Get the search keyword from the query parameters
        if keyword:
            # Perform the search query based on the keyword
            # You can customize the search logic based on your requirements
            results = State.query.join(Region).filter(
                db.or_(
                    Region.name.ilike(f'%{keyword}%'),  # Search by region name
                    State.name.ilike(f'%{keyword}%'),  # Search by state name
                    State.capital.ilike(f'%{keyword}%'),  # Search by state capital
                    Lga.lga_name.ilike(f'%{keyword}%'),  # Search by local government areas
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
    

@search_ns.route('/place')
class RetrieveRegion(Resource):
    # @cache.cached(timeout=60)  # Cache the response for 60 seconds
    # @limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)
    @search_ns.marshal_with(region_model, as_list=True)
    @search_ns.doc(
        description='Get all Places of interest',
    )
    # @jwt_required()
    def get(self):
        places = PlaceOfInterest.query.limit(3).all()
        if places is None:
            return {'message': 'No Place found'}, HTTPStatus.NOT_FOUND

        return places, HTTPStatus.OK


@search_ns.route('/places')
class Places(Resource):
    @search_ns.doc('places_query')
    @search_ns.marshal_with(state_model, lga_model, region_model)
    def get(self):
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
    

# /api/locations?region=<region_name>&state=<state_name>&lga=<lga_name>
# http://127.0.0.1:5000/query/filter?region=South&state=Abia&lga=Umuahia%20North