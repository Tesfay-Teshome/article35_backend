from flask import Flask, Blueprint, request, g
from models.blogs import Blog
from models.comments import Comment, NastedComment
from serializers.blogs import BlogsSchema, PopulateBlogSchema
from serializers.comments import CommetSchema, NestedCommentSchema
from middleware.secure_route import secure_route
from marshmellow import validationError

blog_schema = BlogsSchema()
populate_blog = PopulateBlogSchema()
comment_schema = CommetSchema()
nested_comment_schema = NestedCommentSchema()


route = Blueprint(__name__, 'blogs')

# Get all Blogs

@router.route('/blogs', methods=['GET', 'POST'])
def index():
	blogs = Blog.query.all()
	return blog_schema.jsonify(blogs, many=True), 200

# Get a single blog

@router.route('/blogs/<int:id>', methods=['GET', 'POST'])
def get_single_blog(id):
	blog = Blog.query.get(id)

	if
