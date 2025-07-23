from src.utils.extensions import db
from sqlalchemy.dialects.mysql import JSON

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    # phone = db.Column(db.String(64), unique=True, nullable=True)
    gender = db.Column(db.String(64), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    graduation_year = db.Column(db.String(64), nullable=True)
    education = db.Column(db.String(64), nullable=True)
    university = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)

    # education = db.Column(db.String(64), nullable=True)
    # major = db.Column(db.String(64), nullable=True)
    # experience = db.Column(db.String(64), nullable=True)
    # skills = db.Column(JSON, nullable=True)
    # certs = db.Column(JSON, nullable=True)
    # fresh = db.Column(db.Boolean, nullable=True)

    # skills_type = db.Column(JSON, nullable=True)
    # skills_name = db.Column(JSON, nullable=True)
    # skills_level = db.Column(JSON, nullable=True)
    # skills_scene = db.Column(JSON, nullable=True)
    # skills_filename = db.Column(JSON, nullable=True)

    job_status = db.Column(db.String(64), nullable=True)
    job_position = db.Column(db.String(64), nullable=True)
    job_requirement = db.Column(db.Text, nullable=True)
    job_salary = db.Column(db.String(64), nullable=True)
    job_city = db.Column(db.String(64), nullable=True)
    # introduction = db.Column(db.String(64), nullable=True)

    resume_name = db.Column(db.String(64), nullable=True)