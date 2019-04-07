
import os
from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import EmailData

# The landing page of the accompanying client web app
@app.route('/')
def home():
    emails = EmailData.query.all();
    return render_template('emails.html', emails=emails)

# Form for letting users create an email
# Used in the accompanying web app
@app.route('/create_form', methods=['GET'])
def create_email_display_form():
    return render_template('create.html')

# Form for letting users update an email
# Used in the accompanying web app
@app.route('/update_form', methods=['POST'])
def create_email_edit_form():
    title = request.form.get('title')
    from_email = request.form.get('from_email')
    to_email = request.form.get('to_email')
    email_message = request.form.get('email_message')

    return render_template('update.html', title=title,
                           from_email=from_email,
                           to_email=to_email,
                           email_message=email_message)

# POST method for updating an email record
# Used in the accompanying web app
@app.route('/v1.0/emails/update', methods=['POST'])
def update_email():
    old_title = request.form.get('title_old')
    new_title = request.form.get('title_new')
    from_email = request.form.get('from_email')
    to_email = request.form.get('to_email')
    email_message = request.form.get('email_message')
    email = EmailData.query.filter_by(title=old_title).first()
    email.title = new_title
    email.from_email = from_email
    email.to_email = to_email
    email.email_message = email_message
    db.session.commit()
    return redirect("/")

# POST method for creating an email record
@app.route('/v1.0/emails', methods=['POST'])
def create_email():
    title = request.form.get('title')
    from_email = request.form.get('from_email')
    to_email = request.form.get('to_email')
    email_message = request.form.get('email_message')

    emailData = EmailData(title, from_email, to_email, email_message)
    db.session.add(emailData)
    db.session.commit()

    emails = EmailData.query.all();
    return redirect("/")

# POST method for deleting an email record
# Used in the accompanying web app
@app.route("/v1.0/emails/delete", methods=['POST'])
def delete():
    title = request.form.get("title")
    email = EmailData.query.filter_by(title=title).first()
    db.session.delete(email)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run()
