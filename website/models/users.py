from flask_login import UserMixin
from website.utils.utils import db



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer(), primary_key=True)
    developer_name = db.relationship('User', backref='api_keys')
    key = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, developer_name, key, user_id):
        self.developer_name = developer_name
        self.key = key
        self.user_id = user_id

    def __repr__(self):
        return f"<User {self.user_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
