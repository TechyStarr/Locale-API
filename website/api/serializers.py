import json
from website.models.data import State, Region, Lga
from website.models.auth import User, ApiKey, ResetToken


# data serializer
def serialized_region(region):
    return {
        'id': region.id,
        'name': region.name,
        # 'states': region.states,
    }

def serialized_state(state):
    return {
        'id': state.id,
        'name': state.name,
        'region': state.region,
        'region_id': state.region_id,
        'capital': state.capital,
        'slogan': state.slogan,
        'lgas': state.lgas,  # Convert list to string
        'landmass': state.landmass,
        'population': state.population,
        'dialect': state.dialect,
        'latitude': state.latitude,
        'longitude': state.longitude,
        'website': state.website,
        'borders': state.borders,
        'places_of_interest': state.places_of_interest,
        # 'images': state.images,
        'universities': state.universities,
    }
    


def serialized_lga(lga):
    return {
        'id': lga.id,
        'lga_name': lga.name,
        'state_id': lga.id,
        'landmass': lga.landmass,
        'borders': lga.borders,
    }

def serialized_place_of_interest(place_of_interest):
    return {
        'id': place_of_interest.id,
        'name': place_of_interest.name,
        'location': place_of_interest.location,
        'images': place_of_interest.images,
        'description': place_of_interest.description,
        'state_id': place_of_interest.state_id,
    }

def serialized_border(border):
    return {
        'id': border.id,
        'name': border.name,
        'state_id': border.state_id,
    }

def serialized_university(university):
    return {
        'id': university.id,
        'name': university.name,
        # 'location': university.location,
        'state_id': university.state_id,
    }

def serialized_key(api_key):
    return {
        'key': api_key.key,
        # 'user_id': api_key.user.id if api_key.user else None,
    }

def serialized_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'api_key': user.api_key.key if user.api_key else None,
    }

def serialized_reset_token(reset_token):
    return {
        'id': reset_token.id,
        'token': reset_token.token,
        'user_id': reset_token.user_id,
    }