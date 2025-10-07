from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import bleach

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
Bootstrap5(app)
CKEditor(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = []
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post

@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Clean the HTML content with specific allowed tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3']
        clean_body = bleach.clean(
            form.body.data,
            tags=allowed_tags,
            strip=True  # Strip disallowed tags instead of escaping them
        )
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=clean_body,
            author=form.author.data,
            img_url=form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form)

# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        # Clean the HTML content with specific allowed tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3']
        post.body = bleach.clean(
            form.body.data,
            tags=allowed_tags,
            strip=True  # Strip disallowed tags instead of escaping them
        )
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('make-post.html', form=form)

# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
