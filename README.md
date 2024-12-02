"# Hospital-Management" 

Hospital Management System (HMS)
Welcome to the Hospital Management System developed for Starlight Hospital. This system streamlines hospital operations, including patient management, appointments, and staff records.

Installation and Setup
Follow these steps to set up and run the project:

1. Clone the Repository
git clone <repository_url>
cd <project_directory>

2. Install Dependencies
Ensure you have Python installed (version 3.7 or higher). Then, install the required packages:
pip install -r requirements.txt

3. Update Email Configuration
Edit the EMAIL_HOST and related settings in the settings.py file to match your email service. Locate the following lines in settings.py and update accordingly:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_email_host'
EMAIL_PORT = 587  # or as required
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_password'

4. Apply Migrations
Run the following commands to set up the database:
python manage.py makemigrations
python manage.py migrate

5. Create a Superuser
Create an admin account for managing the system:
python manage.py createsuperuser

6. Run the Development Server
Start the development server:
python manage.py runserver

7. Access the Application
Open your browser and go to:
http://127.0.0.1:8000


Features
admin role is superuser 
Patient management (registration, updates, records)
Appointment scheduling
Staff management (doctors, nurses, admin staff)
Billing and reports
Role-based access control (Admin, Doctor, Receptionist)
