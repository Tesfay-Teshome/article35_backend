from flask import Flask, Blueprint, request, g
from models.blogs import Blog
from models.comments import Comment, NastedComment
from serializers.blogs import BlogsSchema, PopulateBlogSchema
from serializers.comments import CommetSchema, NestedCommentSchema
from securerouter.secure_route import secure_route
from marshmellow import ValidationError

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
		return{'errors': e.messages, 'message': 'Something went wrong.'}, 401

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
		return {'errors': e.message, 'message': 'Something went wrong.'}

	if blog.user != g.current_user:
		return {'message': 'Unauthorized User' }, 401

	blog.save()
	return blog_schema.jsonify(blog), 201

# Delete Blog

@router.route('/blogs/<int:id>', methods=['DELETE'])
def remove(id):
	blog = Blog.query.get(id)

	if blog.user != g.current_user:
		return {'message': 'Unauthorized User'}, 401

	blog.remove()
	return {'message': f'Blog {id}--deleted Successfuly'}

# Post a comment

@router.route('blogs/<int:id>/comments', methods=['POST'])
@secure_route
def comment_create(blog_id):
	comment_data = request.get_json()
	blog = Blog.query.get(blog_id)
	comment = comment_schema.load(comment_data)
	comment.blog = blog
	comment.user.id = g.current_user.id
	comment.save()
	return populate_blog.jsonify(blog), 200

# Get one comment
@router.route('comments/<int:id>', methods=['GET'])
def get_single_comment(id):
	comment = Comment.query.get(id)

    
    if not comment:
    	return {'message': 'Blog is not available'}, 404

    return comment_schema.jsonify(comment), 200

# Delete a Comment

@router.route('/comments/<int:id>', methods=['DELETE'])
@secure_route
def removeComment(id):
	comment = Comment.query.get(id)
	blog_id = comment.blog_id
	blog = Blog.query.get(blog_id)

	if comment.user != g.current_user:
		return{'message': 'Unauthorized User'}, 401
	comment.remove()

	return populate_blog.jsonify(blog), 200

# Edit a Comment

@router.route('/comments/<int:id>', methods=['PUT'])
@secure_route
def update_comment(id):

	existing_comment = Comment.query.get(id)

	try:
		comment = comment_schema.load(
			request.get_json(),
			instance=existing_comment,
			partial=True
		)
	except ValidationError as e:
		return{'errors': e.messages, 'message': 'Something went worng'}

	if comment.user != g.current_user:
		return { 'message': 'Unauthorized User' }, 401

	comment.save()

	return {'message': 'Comment updated' }, 201

# Nested comment

@router.route('/comments/<int:id>/nested', methods=['POST'])
@secure_route
def create_nested(comment_id):
	nested_comment_data = request.get_json()
	comment = Comment.query.get(comment_id)
	if not comment:
		return { 'message': 'Comment not available' }, 404

	nested_comment = nested_comment_schema.load(nested_comment_data)
	nested_comment.comment = comment
	nested_comment.user_id = g.current_user
	nested_comment.comment_id = comment_id
	nested_comment.save()

	blog = Blog.query.get(comment.blog_id)

	return populate_blog.jsonify(blog), 200

# Delete nested comment

@router.route('/comments/<int:comment_id>/<int:nested_id>', methods=['DELETE'])
@secure_route
def removeNestedComment(comment_id, nested_id):
    nested_comment = NestedComment.query.get(nested_id)

    if not nested_comment:
    	return { 'message': 'Comment not available' }, 404

    blog_id = comment.blog_id
    blog = Blog.query.get(blog_id)

    if nested_comment.user != g.current_user:
    	return { 'message': 'Unauthorized User' }, 401

    nested_comment.remove()

    return populate_blog.jsonify(blog), 200
