# import json
# from .users import db
# from datetime import datetime



# class State(db.Model):
#     __tablename__ = 'states'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     region = db.relationship('Region', backref='states')
#     region_id = db.Column(db.Integer(), db.ForeignKey('regions.id'), nullable=False)
#     capital = db.Column(db.String(50), nullable=False)
#     slogan = db.Column(db.String(50), nullable=False)
#     lgas = db.Column(db.String(500), nullable=False)
#     landmass = db.Column(db.String(50), nullable=False)
#     population = db.Column(db.String(50), nullable=False)
#     dialect = db.Column(db.String(50), nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     website = db.Column(db.String(50), nullable=False)
#     borders = db.Column(db.String(200), nullable=False)
#     places_of_interest = db.relationship('PlaceOfInterest', backref='state', lazy=True)
#     # universities = db.Column(db.String(200), nullable=False)


#     def __init__(self, name, region, region_id, capital, slogan, lgas, landmass, population, dialect,
#                 latitude, longitude, website, borders, places_of_interest, universities):
#         self.name = name
#         # self.region = region
#         self.region_id = region_id
#         self.capital = capital
#         self.slogan = slogan
#         self.lgas = json.dumps(lgas)  # Convert list to JSON string
#         self.landmass = landmass
#         self.population = population
#         self.dialect = dialect
#         self.latitude = latitude
#         self.longitude = longitude
#         self.website = website
#         self.borders = json.dumps(borders)  # Convert list to JSON string
#         self.places_of_interest = places_of_interest  
#         # self.universities = universities

#     def __repr__(self):
#         return f"<State {self.name}>"

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)
    

#     # Define an index on the 'name' column
#     __table_args__ = (
#         db.Index('idx_states_name', 'name'),
#     )


# class PlaceOfInterest(db.Model):
#     __tablename__ = 'place_of_interest'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     images = db.Column(db.String(200), nullable=True)
#     description = db.Column(db.String(2000), nullable=False)
#     state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

#     def __init__(self, name, location, images, description, state_id):
#         self.name = name
#         self.location = location
#         self.images = json.dumps(images)
#         self.description = description
#         self.state_id = state_id

    
#     def __repr__(self):
#         return f"<PlacesOfInterest {self.name}>"

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)
    

#     # Define an index on the 'name' column
#     __table_args__ = (
#         db.Index('idx_PlacesOfInterest_name', 'name'),
#     )

# # class Border(db.Model):
# #     __tablename__ = 'borders'
# #     id = db.Column(db.Integer(), primary_key=True)
# #     name = db.Column(db.String(45), nullable=False)
# #     state = db.relationship('State', backref='borders', lazy=True)


# #     def __repr__(self):
# #         return f"<Border {self.name}>"


# #     def save(self):
# #         db.session.add(self)
# #         db.session.commit()

# #     @classmethod
# #     def get_by_id(cls, id):
# #         return cls.query.get_or_404(id)
    
# #     __table_args__ = (
# #         db.Index('idx_borders_name', 'name'),
# #     )

# class Region(db.Model):
#     __tablename__ = 'regions'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(45), nullable=False)
#     state = db.relationship('State', backref='regions', lazy=True)

#     def __repr__(self):
#         return f"<Region {self.name}>"

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)
    
#     __table_args__ = (
#         db.Index('idx_regions_name', 'name'),
#     )



# class Lga(db.Model):
#     __tablename__ = 'lgas'
#     id = db.Column(db.Integer(), primary_key=True)
#     lga_name = db.Column(db.String(45), nullable=False, unique=True)
#     state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
#     landmass = db.Column(db.String(45), nullable=False)
#     borders = db.Column(db.String(100))


#     def __init__(self, lga_name, state_id, landmass, borders):
#         self.lga_name = lga_name
#         self.state_id = state_id
#         self.landmass = landmass
#         self.borders = json.dumps(borders)



#     def __repr__(self):
#         return f"<Lga {self.lga_name}>"

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)
    
#     __table_args__ = (
#         db.Index('idx_lgas_name', 'lga_name'),
#     )
    



# def load_dataset():
#     with open('website/models/dataset.json', 'r', encoding='utf-8') as file:
#         dataset = json.load(file)

#     for region_data in dataset['Regions']:
#         region = Region(name=region_data['name'])
#         db.session.add(region)

#     for state_data in dataset['States']:
#         places_of_interest = []  # Initialize places_of_interest as an empty list
#         for place_of_interest in state_data['places_of_interest']:
#             place = PlaceOfInterest(
#                 name=place_of_interest['name'] if 'name' in place_of_interest else '',
#                 location=place_of_interest['location'] if 'location' in place_of_interest else '',
#                 images= place_of_interest['images'] if 'images' in place_of_interest else '',
#                 description=place_of_interest['description'] if 'description' in place_of_interest else '',
#                 state_id=None  # Set the state_id to None for now
#             )
#             places_of_interest.append(place)

#     for lga_data in dataset['States']:
#         lgas = []  # Initialize lgas as an empty list
#         for lga_in_state in state_data['lgas']:
#             lga = Lga(
#                 lga_name=lga_data['lga_name'] if 'lga_name' in lga_in_state else '',
#                 state_id=lga_data['state_id'] if 'state_id' in lga_in_state else '' ,
#                 landmass=lga_data['landmass'] if 'landmass' in lga_in_state else '' ,
#                 borders=lga_data['borders'] if 'borders' in lga_in_state else '' ,
#             )
#             lgas.append(lga)

#         # del state_data['places_of_interest']
#         state = State(
#             name=state_data['state'],
#             region=state_data['region'],
#             region_id=state_data['region_id'],
#             capital=state_data['capital'],
#             slogan=state_data['slogan'],
#             lgas=state_data['lgas'],
#             landmass=state_data['landmass'],
#             population=state_data['population'],
#             dialect=state_data['dialect'],
#             latitude=state_data['latitude'],
#             longitude=state_data['longitude'],
#             website=state_data['website'],
#             borders=state_data['borders'],
#             places_of_interest=places_of_interest,  # Assign the places_of_interest list to state,  since it is a relationship
#             universities=state_data.get('universities'),
#         )

#         db.session.add(state)

#     for lga_data in dataset['LGAs']:
#         lga = Lga(
#             lga_name=lga_data.get('lga_name'),
#             state_id=lga_data.get('state_id'),
#             landmass=lga_data.get('landmass'),
#             borders=lga_data.get('borders')
#         )
#         db.session.add(lga)

#     db.session.commit()








import json
from .users import db
from datetime import datetime



class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    region_id = db.Column(db.Integer(), db.ForeignKey('regions.id'), nullable=False)
    capital = db.Column(db.String(50), nullable=False)
    slogan = db.Column(db.String(50), nullable=False)
    lgas = db.Column(db.String(500), nullable=False)  # Store LGAs as a JSON string
    landmass = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    dialect = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    website = db.Column(db.String(50), nullable=False)
    borders = db.relationship('Border', backref='state', lazy=True)
    places_of_interest = db.relationship('PlaceOfInterest', backref='state', lazy=True)
    universities = db.relationship('University', backref='state', lazy=True)


    def __init__(self, name, region, region_id, capital, slogan, lgas, landmass, population, dialect,
                latitude, longitude, website, places_of_interest):
        self.name = name
        self.region = region
        self.region_id = region_id
        self.capital = capital
        self.slogan = slogan
        self.lgas = json.dumps(lgas)  # Convert list to JSON string
        self.landmass = landmass
        self.population = population
        self.dialect = dialect
        self.latitude = latitude
        self.longitude = longitude
        self.website = website
        # self.borders = borders  # Convert list to JSON string
        self.places_of_interest = places_of_interest
        # self.universities = universities

    def __repr__(self):
        return f"<State {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    # Define an index on the 'name' column
    __table_args__ = (
        db.Index('idx_states_name', 'name'),
    )


class Border(db.Model):
    __tablename__ = 'borders'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    def __repr__(self):
        return f"<Border {self.name}>"


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    __table_args__ = (
        db.Index('idx_borders_name', 'name'),
    )


class PlaceOfInterest(db.Model):
    __tablename__ = 'place_of_interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    images = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(2000), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    def __init__(self, name, location, images, description, state_id):
        self.name = name
        self.location = location
        self.images = json.dumps(images)
        self.description = description
        self.state_id = state_id

    
    def __repr__(self):
        return f"<PlacesOfInterest {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    # Define an index on the 'name' column
    __table_args__ = (
        db.Index('idx_PlacesOfInterest_name', 'name'),
    )
    

class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # location = db.Column(db.String(100), nullable=False)
    # images = db.Column(db.String(200), nullable=True)
    # description = db.Column(db.String(2000), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    def __init__(self, name, location, images, description, state_id):
        self.name = name
        # self.location = location
        # self.images = json.dumps(images)
        # self.description = description
        self.state_id = state_id

    
    def __repr__(self):
        return f"<University {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    # Define an index on the 'name' column
    __table_args__ = (
        db.Index('idx_universities_name', 'name'),
    )




class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    state = db.relationship('State', backref='regions', lazy=True)


    def __repr__(self):
        return f"<Region {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    __table_args__ = (
        db.Index('idx_regions_name', 'name'),
    )



class Lga(db.Model):
    __tablename__ = 'lgas'
    id = db.Column(db.Integer(), primary_key=True)
    lga_name = db.Column(db.String(45), nullable=False, unique=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    landmass = db.Column(db.String(45), nullable=False)
    borders = db.Column(db.String(100))


    def __init__(self, lga_name, state_id, landmass, borders):
        self.lga_name = lga_name
        self.state_id = state_id
        self.landmass = landmass
        self.borders = json.dumps(borders)



    def __repr__(self):
        return f"<Lga {self.lga_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    __table_args__ = (
        db.Index('idx_lgas_name', 'lga_name'),
    )
    



def load_dataset():
    with open('website/models/dataset.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    for region_data in dataset['Regions']:
        region = Region(name=region_data['name'])
        db.session.add(region)

    for state_data in dataset['States']:
        places_of_interest = []  # Initialize places_of_interest as an empty list
        for place_of_interest in state_data['places_of_interest']:
            place = PlaceOfInterest(
                name=place_of_interest['name'] if 'name' in place_of_interest else '',
                location=place_of_interest['location'] if 'location' in place_of_interest else '',
                images= place_of_interest['images'] if 'images' in place_of_interest else '',
                description=place_of_interest['description'] if 'description' in place_of_interest else '',
                state_id=None  # Set the state_id to None for now
            )
            places_of_interest.append(place)

        # borders = []  # Initialize borders as an empty list
        # if 'borders' in state_data and isinstance(state_data['borders'], list):
        #     for border_data in state_data['borders']:
        #         border = Border(name=border_data) if 'name' in border_data else ''
        #         borders.append(border)

        # universities = []  # Initialize universities as an empty list
        # for university_data in state_data['universities']:
        #     university = University(name=university_data['name']) if 'name' in university_data else ''
        #     universities.append(university)
    
        

        # del state_data['places_of_interest']
        state = State(
            name=state_data['state'],
            region=state_data['region'],
            region_id=state_data['region_id'],
            capital=state_data['capital'],
            slogan=state_data['slogan'],
            lgas=state_data['lgas'],
            landmass=state_data['landmass'],
            population=state_data['population'],
            dialect=state_data['dialect'],
            latitude=state_data['latitude'],
            longitude=state_data['longitude'],
            website=state_data['website'],
            # borders=borders,
            places_of_interest=places_of_interest,  # Assign the places_of_interest list to state
            # universities=universities
        )

        db.session.add(state)

    for lga_data in dataset['LGAs']:
        lga = Lga(
            lga_name=lga_data.get('lga_name'),
            state_id=lga_data.get('state_id'),
            landmass=lga_data.get('landmass'),
            borders=lga_data.get('borders')
        )
        db.session.add(lga)

    db.session.commit()