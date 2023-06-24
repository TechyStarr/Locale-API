import json
from .users import db
from datetime import datetime






class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(45), nullable=False)
    region_id = db.Column(db.Integer(), db.ForeignKey('regions.id'), nullable=False)
    capital = db.Column(db.String(50), nullable=False)
    slogan = db.Column(db.String(50), nullable=False)
    lgas = db.Relationship('Lga', backref='states', lazy=True)
    landmass = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    dialect = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    website = db.Column(db.String(50), nullable=False)
    borders = db.Column(db.String(200), nullable=False)
    known_for = db.Column(db.String(200), nullable=False)

    def __init__(self, name, region, region_id, capital, slogan, lgas, landmass, population, dialect,
                latitude, longitude, website, borders, known_for):
        self.name = name
        self.region = region
        self.region_id = region_id
        self.capital = capital
        self.slogan = slogan
        self.lgas = lgas
        self.landmass = landmass
        self.population = population
        self.dialect = dialect
        self.latitude = latitude
        self.longitude = longitude
        self.website = website
        self.borders = json.dumps(borders)  # Convert list to JSON string
        self.known_for = json.dumps(known_for)  # Convert list to JSON string




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
    state_id = db.Column(db.Integer(), db.ForeignKey('states.id'), nullable=False)
    # state = db.Column(db.String(45), nullable=False)
    landmass = db.Column(db.String(45), nullable=False)
    borders = db.Column(db.String(100))

    def __repr__(self):
        return f"<City {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    state_id = db.Column(db.Integer(), db.ForeignKey('states.id'), nullable=False)
    city_id = db.Column(db.Integer(), db.ForeignKey('cities.id'), nullable=False)

    def __repr__(self):
        return f"<Area {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    region_id = db.Column(db.Integer(), db.ForeignKey('regions.id'), nullable=False)
    areas = db.relationship('Area', backref='city', lazy=True)

    def __repr__(self):
        return f"<City {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    



def load_dataset():
    with open('website/models/dataset.json') as file:
        dataset = json.load(file)

    for region_data in dataset['Regions']:
        region = Region(name=region_data['name'])
        db.session.add(region)

    for state_data in dataset['States']:
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
            borders=state_data['borders'],
            known_for=state_data['known_for'],
        )
        
        # Retrieve the LGAs from the database based on their names
        lgas = Lga.query.filter(Lga.lga_name.in_(state_data['lgas'])).all()
        state.lgas = lgas
        
        db.session.add(state)

    for lga_data in dataset['LGAs']:
        lga = Lga(
            lga_name=lga_data.get('lga_name'),
            state_id=lga_data.get('state_id'),
            # state=lga_data.get('state'),
            landmass=lga_data.get('landmass'),
            borders=lga_data.get('borders'),
        )
        print(lga)
        db.session.add(lga)



    # Add other models and relationships based on your dataset structure

    db.session.commit()
