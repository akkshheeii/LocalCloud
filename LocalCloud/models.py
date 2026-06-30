from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin,db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    storage_limit = db.Column(
        db.Integer,
        default=10737418240
    )

    storage_used = db.Column(
        db.Integer,
        default=0
    )

class File(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    filepath = db.Column(
        db.String(500),
        nullable=False
    )

    file_size = db.Column(
        db.Integer
    )

    filetype = db.Column(
        db.String(50),
        nullable=False
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

