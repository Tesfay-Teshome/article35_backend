from app import db
from models.base import BaseModel
from models.user import User

class Blog(db.Model, BaseModel):
	__tablename__ = 'blogs'
    title = db.Column(db.String(150), nullable=False)
    blogData = db.Column(db.String(20000), nullable=False)
    imageUrl = db.Column(db.String(10000), nullable=False)
    checked = db.Column(db.Boolean, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    user = db.relationship('User', backref='blogs')