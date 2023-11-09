 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soccer.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Post %r>' % self.title

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Topic %r>' % self.title

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/forum')
def forum():
    topics = Topic.query.all()
    return render_template('forum.html', topics=topics)

@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get(topic_id)
    return render_template('topic.html', topic=topic)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('create_post.html')

@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        topic = Topic(title=title, body=body)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('forum'))
    return render_template('create_topic.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
