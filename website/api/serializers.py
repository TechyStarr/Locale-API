from website.models.data import State, Region, Lga
# from website.models.users import User

# user serializer






# data serializer
def serialized_region(region):
    return {
        'id': region.id,
        'name': region.name,
    }

def serialized_state(state):
    return {
        'id': state.id,
        'name': state.name,
        'region_id': state.region_id,
        'capital': state.capital,
        'population': state.population,
        'area': state.area,
        # 'No_of_LGAs': state.No_of_LGAs,
        'lgas': state.lgas
    }


def serialized_lga(lga):
    return {
        'id': lga.id,
        'name': lga.name,
        'state_id': lga.state_id,
        'state': lga.state,
        'area': lga.area,
        'population': lga.population,
        'headquarters': lga.headquarters
    }

