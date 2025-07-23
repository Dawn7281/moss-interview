from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class QA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_role = db.Column(db.String(64), nullable=False)
    candidate_skill = db.Column(db.String(64), nullable=False)
    role_description = db.Column(db.Text, nullable=False)
    questions = db.Column(JSON, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
