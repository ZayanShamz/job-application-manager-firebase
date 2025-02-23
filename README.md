# Job Application Tracker - Flask Web Application

This is a **Job Application Tracker** web application built using **Python Flask** for the backend, **HTML/CSS** for the frontend, and **Firebase** for authentication and real-time database management. The application allows users to register, log in, and track their job applications. Users can add, edit, delete, and view details of their job applications.

---

## Features

- **User Authentication**: Register and log in using Firebase Authentication.
- **Job Application Management**:
  - Add new job applications with details like company name, job title, description, requirements, platform, and date.
  - Edit existing job applications.
  - Delete job applications.
  - View detailed information about each job application.
- **Real-Time Database**: All data is stored and managed using Firebase Realtime Database.
- **Responsive Design**: Simple and user-friendly interface.

---

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML, CSS
- **Database**: Firebase Realtime Database
- **Authentication**: Firebase Authentication
- **Environment Management**: `python-dotenv` for managing environment variables.

---

## Setup Instructions

### Prerequisites

- Python 3.x installed.
- Firebase project with Authentication and Realtime Database enabled.
- Firebase Admin SDK credentials (JSON file).

### Steps to Run Locally

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Install dependencies**:

   ```bash
   pip install flask pyrebase python-dotenv firebase-admin
   ```

3. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     FIREBASE_API_KEY=<your-firebase-api-key>
     FIREBASE_AUTH_DOMAIN=<your-firebase-auth-domain>
     FIREBASE_DATABASE_URL=<your-firebase-database-url>
     FIREBASE_PROJECT_ID=<your-firebase-project-id>
     FIREBASE_STORAGE_BUCKET=<your-firebase-storage-bucket>
     FIREBASE_MESSAGING_SENDER_ID=<your-firebase-messaging-sender-id>
     FIREBASE_APP_ID=<your-firebase-app-id>
     FIREBASE_MEASUREMENT_ID=<your-firebase-measurement-id>
     FIREBASE_SERVICE_ACCOUNT_KEY_PATH=<path-to-service-account-key.json>
     FLASK_KEY=<your-flask-secret-key>
     ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open your browser and go to `http://localhost:5005`.

---

## Routes

- **`/`**: Login page.
- **`/register`**: Registration page.
- **`/home`**: Home page (displays list of job applications).
- **`/dashboard/<job_id>`**: Detailed view of a specific job application.
- **`/edit/<job_id>`**: Edit a specific job application.
- **`/delete/<job_id>`**: Delete a specific job application.
- **`/logout`**: Log out the user.

---

## Notes

- Ensure the `.env` file and Firebase Admin SDK JSON file are not exposed publicly.
- The application uses Firebase Authentication and Realtime Database, so ensure your Firebase project is properly configured.

---

Enjoy tracking your job applications! 🚀
