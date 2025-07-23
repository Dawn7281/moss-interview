from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(JSON, nullable=True)
    value = db.Column(JSON, nullable=True)