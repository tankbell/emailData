## Application to store and send emails

### Tech Stack
1. Python
2. Redis for the messaging queue
3. sendgrid for sending the emails
4. Heroku [PaaS for hosting the app]
5. Postgres as the backend data store
6. HTML / CSS (bootstrap) for the front end

### Brief Description

Application can be accessed at : https://email-data-2019.herokuapp.com/ 

Additionally , the next section lists the CRUD apis tested using curl.

Use the “Create New Email” button to create your email. The backend assigns an auto incrementing id to each email record that was created. This id serves as the primary key for the data.

Use the “Send Emails” button to bulk send your emails. The emails are enqueued [**published**] to a Redis queue and the send_email_worker process [**subscriber**] does the following : 
1. Sends the email using sendgrid
2. If the error code is OK , updates the record in the database with the “Email Sent” flag set to true.

**Please make sure to check your spam folder for the email that was sent.**

On heroku , the redis server [used as a messaging queue] and postgres DB are installed as add-ons and run on their own pods.

Typically on heroku for larger projects , one process is run per dyno . So the web app , rest service and the send_email_worker process should each run on their own dockerized pods.

In this case however , the web app is demonized as a background process and the send_email_worker process runs in the foreground and they are both run as part of the web process as defined in the Procfile.

The dockerization of the web app , rest service and send_email_worker processes are left as an exercise under the “Future Work” section.

### REST APIs (tested using curl)

1. **CREATE new record**

curl -d '{"title":"Test", "from_email":"ram.kulathumani@gmail.com","to_email":"ram.sunnyvale@gmail.com","email_message":"Test"}' -H "Content-Type: application/json" -X POST https://email-data-2019.herokuapp.com/api/v1.0/emails

Response : Returns all data along with the newly added one

Sample Response :

[{"id": "5", "title": "Welcome to San Francisco", "from_email": "ram.kulathumani@gmail.com", "to_email": "gayathri.ravichandran@gmail.com", "email_message": "Welcome to the city ! Check your spam folder ! ", "email_sent": "True"}, {"id": "9", "title": "Test", "from_email": "ram.kulathumani@gmail.com", "to_email": "ram.sunnyvale@gmail.com", "email_message": "Test", "email_sent": "False"}]

2. **Read all records in the DB**

curl -i -H "Content-Type: application/json" -X GET https://email-data-2019.herokuapp.com/api/v1.0/emails

Response : Returns all the data in the DB

Sample Response :

HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Mon, 08 Apr 2019 14:38:44 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 230
Via: 1.1 vegur

[{"id": "5", "title": "Welcome to San Francisco", "from_email": "ram.kulathumani@gmail.com", "to_email": "gayathri.ravichandran@gmail.com", "email_message": "Welcome to the city ! Check your spam folder ! ", "email_sent": "True"}]

3. **Read record given it’s ID**

curl -i -H "Content-Type: application/json" -X GET https://email-data-2019.herokuapp.com/api/v1.0/emails/5

Response : Returns the row with the specified ID in the API

Sample Response :

HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Mon, 08 Apr 2019 14:40:47 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 228
Via: 1.1 vegur

{"id": "5", "title": "Welcome to San Francisco", "from_email": "ram.kulathumani@gmail.com", "to_email": "gayathri.ravichandran@gmail.com", "email_message": "Welcome to the city ! Check your spam folder ! ", "email_sent": "True"}

4. **Update record given it’s ID**

(Change the title in this example)

curl -d '{"title":"Change Title", "from_email":"ram.kulathumani@gmail.com","to_email":"ram.sunnyvale@gmail.com","email_message":"Test"}' -H "Content-Type: application/json" -X PUT https://email-data-2019.herokuapp.com/api/v1.0/emails/10

Response : Returns all records in the DB along with the updated one.

Sample Response :

[{"id": "5", "title": "Welcome to San Francisco", "from_email": "ram.kulathumani@gmail.com", "to_email": "gayathri.ravichandran@gmail.com", "email_message": "Welcome to the city ! Check your spam folder ! ", "email_sent": "True"}, {"id": "10", "title": "Change Title", "from_email": "ram.kulathumani@gmail.com", "to_email": "ram.sunnyvale@gmail.com", "email_message": "Test", "email_sent": "False"}]

5. **Delete record given it’s ID**

curl -i -X DELETE http://email-data-2019.herokuapp.com/api/v1.0/emails/10

Response : Returns the remaining data in the DB (minus the deleted one)

Sample Response :

[{"id": "5", "title": "Welcome to San Francisco", "from_email": "ram.kulathumani@gmail.com", "to_email": "gayathri.ravichandran@gmail.com", "email_message": "Welcome to the city ! Check your spam folder ! ", "email_sent": "True"}]

6. **Delete all records in the DB**

curl -i -X DELETE http://email-data-2019.herokuapp.com/api/v1.0/emails

Response : Empty json

Sample Response :

HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Mon, 08 Apr 2019 14:50:14 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 2
Via: 1.1 vegur

[]

### Future Work

1. Detailed error handling [pretty messages , returning detailed error codes etc]
2. Dockerize
3. Scaling [both for REST apis and the send email messaging queue and worker process]


