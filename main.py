from flask import Flask, render_template, url_for
import requests

posts = requests.get("https://api.npoint.io/83360257fa3216999b66").json()
post_objects = []
for post in posts:
    post_objects.append({
        "id": post["id"],
        "title": post["title"],
        "subtitle": post["subtitle"],
        "body": post["body"]
    })

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', header_image=url_for('static', filename='assets/img/home-bg.jpg'), all_posts=post_objects)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/about')
def about():
    return render_template('about.html', header_image=url_for('static', filename='assets/img/about-bg.jpg'))

@app.route('/contact')
def contact():
    return render_template('contact.html', header_image=url_for('static', filename='assets/img/contact-bg.jpg'))

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in post_objects:
        if post["id"] == index:
            requested_post = post
    return render_template('post.html', header_image=url_for('static', filename='assets/img/post-bg.jpg'), post=requested_post)