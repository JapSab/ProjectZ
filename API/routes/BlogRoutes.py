from API import app, blogs_collection
from flask import request, jsonify
from API.classes.Blog import Blogger
from API.jwt_token.tokenizer import admin_required


blogger = Blogger(blogs_collection)


@app.route('/api/blogs', methods=['POST'])
# @admin_required
def create_blog():
    data = request.json
    response = blogger.create_blog(data['title'], data['content'])
    return jsonify(response), 201

@app.route('/api/blogs/<blog_id>', methods=['GET'])
def read_blog(blog_id):
    response = blogger.get_blog(blog_id)
    if "message" in response and response["message"] == "Blog not found":
        return jsonify(response), 404
    return jsonify(response), 200

@app.route('/api/blogs/recent', methods=['GET'])
def read_recent_blogs():
    blogs = blogger.get_recent_blogs()
    return jsonify(blogs), 200

@app.route('/api/blogs/<blog_id>', methods=['PUT'])
# @admin_required
def update_blog(blog_id):
    data = request.json
    response = blogger.update_blog(blog_id, data['title'], data['content'])
    if "not found" in response["message"]:
        return jsonify(response), 404
    return jsonify(response), 200

@app.route('/api/blogs/<blog_id>', methods=['DELETE'])
# @admin_required
def delete_blog(blog_id):
    response = blogger.delete_blog(blog_id)
    if "not found" in response["message"]:
        return jsonify(response), 404
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)