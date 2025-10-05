from flask import Flask, render_template, url_for, request
import requests
import os
import smtplib
from email.message import EmailMessage
import dotenv
dotenv.load_dotenv()

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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]

        # Email setup
        EMAIL_ADDRESS = os.environ.get('BLOG_EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('BLOG_EMAIL_PASS')
        RECEIVER_EMAIL = email

        email_message = EmailMessage()
        email_message['Subject'] = f'New Contact Form Submission from {name}'
        email_message['From'] = EMAIL_ADDRESS
        email_message['To'] = EMAIL_ADDRESS
        email_message.set_content(f"""
Name: {name}
Email: {email}
Phone: {phone}
Message: {message}
        """)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(email_message)
        except Exception as e:
            print(f"Error sending email: {e}")
            return render_template('contact.html', header_image=url_for('static', filename='assets/img/contact-bg.jpg'), header_title="Error sending message", header_subtitle="Please try again later.")

        return render_template('contact.html', header_image=url_for('static', filename='assets/img/contact-bg.jpg'), header_title="Successfully sent message", header_subtitle="Thank you for reaching out!")
    else:
        return render_template('contact.html', header_image=url_for('static', filename='assets/img/contact-bg.jpg'), header_title="Contact Me", header_subtitle="Have questions? I have answers.")





@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in post_objects:
        if post["id"] == index:
            requested_post = post
    return render_template('post.html', header_image=url_for('static', filename='assets/img/post-bg.jpg'), post=requested_post)

