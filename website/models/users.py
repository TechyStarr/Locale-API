from flask_login import UserMixin
from website.utils.utils import db



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        # self.is_authenticated = True




    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
