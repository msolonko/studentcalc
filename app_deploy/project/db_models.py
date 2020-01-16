from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #general / login
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    #stats / demographics
    gpa = db.Column(db.Float, nullable=True)
    test = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    race = db.Column(db.Integer, nullable=True)
    essay = db.Column(db.Float, nullable=True)
    recommendation = db.Column(db.Float, nullable=True)
    school = db.Column(db.Float, nullable=True)
    region = db.Column(db.Integer, nullable=True)
    sat2_avg = db.Column(db.Integer, nullable=True)
    sat1 = db.Column(db.Integer, nullable=True)
    sat2 = db.Column(db.Integer, nullable=True)
    sat3 = db.Column(db.Integer, nullable=True)
    sat4 = db.Column(db.Integer, nullable=True)
    sat5 = db.Column(db.Integer, nullable=True)
    
    #booleans
    stats_step = db.Column(db.Boolean, nullable=False, default=False)
    award_step = db.Column(db.Boolean, nullable=False, default=False)
    activity_step = db.Column(db.Boolean, nullable=False, default=False)
    show_modal = db.Column(db.Boolean, nullable=False, default=True)
    
    #scores
    tier1 = db.Column(db.Float, nullable=True)
    tier2 = db.Column(db.Float, nullable=True)
    tier3 = db.Column(db.Float, nullable=True)
    tier4 = db.Column(db.Float, nullable=True)
    award_score = db.Column(db.Float, nullable=True)
    activity_score = db.Column(db.Float, nullable=True)
    
    #relationships
    awards = db.relationship('Award', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.email}')"
    

class Award(db.Model):
    __tablename__ = 'awards'
    id = db.Column(db.Integer, primary_key=True)
    award_type = db.Column(db.Integer, nullable=False)
    check = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Award('{self.award_type}')"
    
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    activity_type = db.Column(db.Integer, nullable=False)
    impact = db.Column(db.Boolean, nullable=False)
    leadership = db.Column(db.Boolean, nullable=False)
    years = db.Column(db.Float, nullable=False)
    weeks = db.Column(db.Float, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    time_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Activity('{self.name}')"
