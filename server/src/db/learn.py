from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class Learn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=True)
    value = db.Column(JSON, nullable=True)