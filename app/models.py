from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    documents = db.relationship('Document', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    original_filename = db.Column(db.String(100))
    file_path = db.Column(db.String(200))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expiration_date if self.expiration_date else False

    def time_remaining(self):
        if not self.expiration_date:
            return None
        remaining = self.expiration_date - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else None
