from flask import Flask, session, request, render_template, redirect, url_for
import pyrebase
import os
from dotenv import load_dotenv
import base64
import json
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import UserNotFoundError, get_user_by_email


load_dotenv()


encoded_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
decoded_json = json.loads(base64.b64decode(encoded_json).decode())

# Initialize Firebase Admin SDK
cred = credentials.Certificate(decoded_json)
firebase_admin.initialize_app(cred)


config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_KEY')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            session['localId'] = user['localId']
            session['idToken'] = user['idToken']
            return redirect(url_for('home'))
        except:
            return "<script>alert('Invalid Credentials');window.location='/';</script>"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            # Check if the email already exists using Firebase Admin SDK
            user = get_user_by_email(email)
            return "<script>alert('Email Already Exists!');window.location='/register';</script>"

        except UserNotFoundError:
            # Create a new user if the email is not found
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)
                session['user'] = user
                session['localId'] = user['localId']
                session['idToken'] = user['idToken']

                # Store additional user info
                data = {'username': username}

                db.child("users").child(user['localId']).child(
                    "info").set(data, session['idToken'])
                return redirect(url_for('home'))

            except Exception as e:
                print(f"Error creating user: {e}")
                return "<script>alert('Error creating account! Please try again.');window.location='/register';</script>"

        except Exception as e:
            print(f"Unexpected error: {e}")
            return "<script>alert('An error occurred. Please try again.');window.location='/register';</script>"

    else:
        return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    user_id = session['localId']

    user_info = db.child("users").child(
        user_id).child("info").get(session['idToken'])
    username = user_info.val().get('username')

    jobs = db.child("users").child(user_id).child(
        "jobs").get(session['idToken'])

    job_list = []
    # Loop through the jobs and add the job_id corresponding to the item. firebase doesnt include the id on defualt.
    if jobs.each():
        for job in jobs.each():
            job_data = job.val()  # Get the job data
            # Add the job_id (Firebase's key) to the job data
            job_data['job_id'] = job.key()
            job_list.append(job_data)

    if request.method == 'POST':
        company_name = request.form['company']
        job_title = request.form['jobTitle']
        job_description = request.form['description']
        job_requirements = request.form['requirement']
        platform = request.form['platform']
        date = request.form['date']

        try:
            data = {
                "company_name": company_name,
                "job_title": job_title,
                "job_description": job_description,
                "job_requirements": job_requirements,
                "platform": platform,
                "status": 'Applied',
                "reference": 'reference',
                "date": date
            }

            db.child("users").child(user_id).child(
                "jobs").push(data, session['idToken'])
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            return "Failed to add job"

    return render_template('index.html', jobs=job_list, username=username)


@app.route('/dashboard/<job_id>', methods=['GET', 'POST'])
def dashboard(job_id):
    user_id = session['localId']

    job_data = db.child("users").child(user_id).child(
        "jobs").child(job_id).get(session['idToken'])

    if job_data:
        job = job_data.val()
        print(job)
    return render_template('dashboard.html', job=job, job_id=job_id)


@app.route('/edit/<job_id>', methods=['GET', 'POST'])
def edit(job_id):
    user_id = session['localId']

    job_data = db.child("users").child(user_id).child(
        "jobs").child(job_id).get(session['idToken'])

    if job_data:
        job = job_data.val()

    if request.method == 'POST':
        company_name = request.form['company']
        job_title = request.form['jobTitle']
        job_description = request.form['description']
        job_requirements = request.form['requirement']
        platform = request.form['platform']
        status = request.form['status']
        follow_up = request.form['follow-up']
        date = request.form['date']

        updated_data = {
            "company_name": company_name,
            "job_title": job_title,
            "job_description": job_description,
            "job_requirements": job_requirements,
            "platform": platform,
            "status": status,
            "follow_up": follow_up,
            "date": date
        }

        # Update the job details in Firebase
        db.child("users").child(user_id).child("jobs").child(
            job_id).update(updated_data, session['idToken'])

        return redirect(url_for('dashboard', job_id=job_id))

    return render_template('edit.html', job=job, job_id=job_id)


@app.route('/delete/<job_id>')
def delete(job_id):
    user_id = session['localId']
    try:
        db.child("users").child(user_id).child(
            "jobs").child(job_id).remove(session['idToken'])
        return f"<script>alert('Deleted');window.location='/home';</script>"
    except Exception as e:
        print(e)
        return "Failed to delete job"


@app.route('/logout')
def logout():
    session.clear()
    print("Logout Successfull")
    return redirect(url_for('login'))


@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred. Please try again later.", 500


@app.errorhandler(404)
def not_found(error):
    return "Page not found. Please check the URL.", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
