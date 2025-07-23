from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class InterviewRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    interview_type = db.Column(db.String(64), nullable=False)
    candidate_skill = db.Column(db.String(64), nullable=False)
    job_role = db.Column(db.String(64), nullable=False)
    role_description = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    scene = db.Column(db.String(64), nullable=False)

    chatlog = db.Column(JSON, nullable=False)
    evaluation = db.Column(JSON, nullable=False)
    emotions = db.Column(JSON, nullable=True)
