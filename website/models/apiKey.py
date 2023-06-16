from website.utils.utils import db



class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer(), primary_key=True)
    developer_name = db.Column(db.String(50), nullable=False, unique=True)
    key = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))



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
