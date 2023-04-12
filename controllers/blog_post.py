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

	if not blog:
		return {'message': 'blog not available'}, 404

	return populate_blog.jsonify(blog), 200

# Add a blog

@router.route('/blogs', methods=['POST'])
@secure_route
def create():
	blog_dictionary = request.get_json()
	blog_dictionary['user_id'] = g.current_user.id

	try:
		blog = populate_blog.load(blog_dictionary)
	except ValidationError as e:
		return{'errors': e.messages, 'message': 'Somthing went wrong.'}, 401

	blog.save()

	return populate_blog.jsonify(blog), 200

# Edit a Blog

@router.route('/blogs/<int:id>', method=['PUT'])
@secure_route
def update_blog(id):
	existing_blog = Blog.query.get(id)

	try:
		blog = blog_schema.load(
		  request.get_json(),
		  instance = existing_blog,
		  partial=True
	    )
	except ValidationError as e:
		return {'errors': e.message, 'message': 'Somthing went wrong.'}

	if blog.user != g.current_user:
		return {'message': 'Unauthorized User' }, 401

	blog.save()
	return blog_schema.jsonify(blog), 201

# Delete Blog

@router.route('/blogs/<int:id>', methods=['DELETE'])
def remove(id):
	blog = Blog.query.get(id)

	if video.user != g.current_user:
		return {'message': 'Unauthorized User'}, 401

	blog.remove()
	return {'message':}

