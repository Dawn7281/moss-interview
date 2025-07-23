from src.utils.extensions import db

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    date = db.Column(db.Date, nullable=True)
    continue_count = db.Column(db.Integer, nullable=False)
    total_count = db.Column(db.Integer, nullable=False)