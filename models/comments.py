from app import db 
from modles.base import BaseModel
from models.blogs import Blog
from models.user import User 

class Comment(db.Model, BaseModel):

	__tablename__ = 'comments'


	content = db.Column(db.Text, nullable=False)
	blog_id = db.column(db.Integer, db.ForeignKey('blogs.id'))
	blog = db.relationship('Blog', backref='comments')

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	user = db.relationship('User', backref='comments')

class NestedComment(db.Model, BaseModel):
     
    __tablename__ = 'nested_comments'

    nested_content = db.Column(db.Text, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments_id'))
    comment = db.relationship('Comment', backref='nested_comments')
     
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationships('User', backref='nested_comments')
