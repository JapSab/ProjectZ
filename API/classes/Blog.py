from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId

class Blogger:
    def __init__(self, blogs_collection):
        self.blogs_collection = blogs_collection

    def create_blog(self, title, content):
        current_date = datetime.now().strftime('%d/%m/%y')
        blog_post = {"title": title, "content": content, "date": current_date}
        result = self.blogs_collection.insert_one(blog_post)
        return {"message": "Successfully posted blog.", "blog_id": str(result.inserted_id)}

    def get_blog(self, blog_id):
        try:
            blog = self.blogs_collection.find_one({"_id": ObjectId(blog_id)})
            if blog:
                blog['_id'] = str(blog['_id'])  # Convert ObjectId to string for JSON serialization
                return blog
            else:
                return {"message": "Blog not found"}
        except InvalidId:
            return {"message": "Invalid blog ID format"}

    def get_recent_blogs(self):
        blogs = self.blogs_collection.find().sort("_id", -1).limit(20)
        return [{"_id": str(blog["_id"]), "title": blog["title"], "content": blog["content"], "date": blog["date"]} for blog in blogs]

    def update_blog(self, blog_id, title, content):
        result = self.blogs_collection.update_one({"_id": ObjectId(blog_id)}, {"$set": {"title": title, "content": content}})
        if result.modified_count:
            return {"message": "Blog updated successfully"}
        else:
            return {"message": "Blog not found or not updated"}

    def delete_blog(self, blog_id):
        result = self.blogs_collection.delete_one({"_id": ObjectId(blog_id)})
        if result.deleted_count:
            return {"message": "Blog deleted successfully"}
        else:
            return {"message": "Blog not found or not deleted"}
