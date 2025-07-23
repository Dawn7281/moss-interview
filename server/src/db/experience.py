from src.utils.extensions import db

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    full_content = db.Column(db.Text, nullable=True)
    content_type = db.Column(db.String(64), nullable=False)
    level = db.Column(db.String(64), nullable=False)
    school = db.Column(db.String(64), nullable=True)
    time = db.Column(db.String(64), nullable=False)
