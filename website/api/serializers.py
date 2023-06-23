from website.models.data import State, Region, Lga
# from website.models.users import User

# user serializer






# data serializer
def serialized_region(region):
    return {
        'id': region.id,
        'name': region.name,
        'states': region.states,
    }

def serialized_state(state):
    return {
        'id': state.id,
        'name': state.name,
        'region': state.region,
        'region_id': state.region_id,
        'capital': state.capital,
        'slogan': state.slogan,
        'landmass': state.landmass,
        'population': state.population,
        'dialect': state.dialect,
        'latitude': state.latitude,
        'longitude': state.longitude,
        'website': state.website,
        'date_of_creation': state.date_of_creation,
        'borders': state.borders,
        'known_for': state.known_for,
        # 'No_of_LGAs': state.No_of_LGAs,
        'lgas': state.lgas
    }


def serialized_lga(lga):
    return {
        'id': lga.id,
        'lga_name': lga.name,
        'state_id': lga.state_id,
        'state': lga.state,
        'landmass': lga.landmass,
        'borders': lga.borders,
    }

