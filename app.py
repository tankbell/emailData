
import os
import time
import json
import sendgrid
from collections import OrderedDict
from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from rq import Queue
from rq.job import Job
from send_email_worker import conn
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)

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
    id = request.form.get('id')
    title = request.form.get('title')
    from_email = request.form.get('from_email')
    to_email = request.form.get('to_email')
    email_message = request.form.get('email_message')

    return render_template('update.html',
                           id=id,
                           title=title,
                           from_email=from_email,
                           to_email=to_email,
                           email_message=email_message)

# POST method for updating an email record
# Used in the accompanying web app
@app.route('/v1.0/emails/update', methods=['POST'])
def update_email():
    old_id = request.form.get('id_old')
    new_id = request.form.get('id_new')
    title = request.form.get('title')
    from_email = request.form.get('from_email')
    to_email = request.form.get('to_email')
    email_message = request.form.get('email_message')
    email = EmailData.query.filter_by(id=old_id).first()
    email.id = new_id
    email.title = title
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
    email_sent = "False"

    emailData = EmailData(title, from_email, to_email, email_message, email_sent)
    # Future Work : Add proper error handling here.
    try:
        db.session.add(emailData)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect("/")

# POST method for deleting an email record
# Used in the accompanying web app
@app.route("/v1.0/emails/delete", methods=['POST'])
def delete():
    id = request.form.get("id")
    email = EmailData.query.filter_by(id=id).first()
    db.session.delete(email)
    db.session.commit()
    return redirect("/")

# GET api for getting all the email data
@app.route("/v1.0/emails", methods=['GET'])
def get_emails():
    emails = EmailData.query.all();
    return to_array(emails)

def to_array(all_emails):
    e = [ em.asdict() for em in all_emails ]
    return json.dumps(e) 

def send_emails(email_key,id,title, from_email, to_email, email_message, email_sent):
    sg = sendgrid.SendGridAPIClient(email_key)
    data = {
    "personalizations": [
     {
      "to": [
        {
          "email": to_email
        }
       ],
      "subject": title
     }
    ],
    "from": {
      "email": from_email
    },
    "content": [
     {
      "type": "text/plain",
      "value": email_message
     }
    ]
    }
    response = sg.client.mail.send.post(request_body=data)
    rc = response.status_code
    print(rc)
    if (rc == 202):
        email = EmailData.query.filter_by(id=id).first()
        print (email.email_message)
        print (email.email_sent)
        email.email_sent = "True"
        db.session.commit()



@app.route('/v1.0/emails/publish')
def publish_to_queue():
    email_api_key = os.environ.get('SENDGRID_API_KEY')
    emails = EmailData.query.all();
    for email in emails:
        if email.email_sent=="True":
            continue
        q.enqueue_call(func=send_emails,
            args=(email_api_key,email.id,email.title, email.from_email, email.to_email, email.email_message, email.email_sent),
            result_ttl=5000)
    return redirect("/")


if __name__ == '__main__':
    app.run()
