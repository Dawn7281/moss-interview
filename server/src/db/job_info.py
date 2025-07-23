from src.utils.extensions import db

class JobInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Text, nullable=False)
    industry = db.Column(db.Text, nullable=False)
    scale = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    education = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    postTime = db.Column(db.Text, nullable=False)