from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author_posts', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='posts')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref='comments')



# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data['title']
    content = data['content']
    author_id = data['author_id']
    category_id = data['category_id']
    post = Post(title=title, content=content, author_id=author_id, category_id=category_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully!'})



if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
