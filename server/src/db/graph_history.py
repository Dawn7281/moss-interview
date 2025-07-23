from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class GraphHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    graph_id = db.Column(db.Integer, nullable=False)
    search_keyword = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
