# registration_QR_CodeRegistration QR Code Project
This project is a web-based application that allows users to register and generate a unique QR code associated with their user ID. The application is built using Flask, a Python web framework, and utilizes a MySQL database to store user information.

Features
User registration with username, phone number, email, occupation, state, and city
Generation of a unique QR code for each registered user
Search functionality to retrieve user information by user ID
Edit functionality to update user information
Print functionality to display the QR code and user ID
Getting Started
Prerequisites
Python 3.x
Flask
MySQL
qrcode library
Installation
Clone the repository: git clone https://github.com/your-username/registration-qr-code.git
Install the required dependencies: pip install -r requirements.txt
Create a MySQL database and update the db_config dictionary in app.py with your database credentials
Run the application: python app.py
Usage
Open a web browser and navigate to http://localhost:5000
Click on the "Register" button to create a new user account
Fill in the registration form and submit to generate a QR code
Use the search functionality to retrieve user information by user ID
Click on the "Edit" button to update user information
Click on the "Print" button to display the QR code and user ID
Directory Structure
app.py: The main application file
templates: Directory containing HTML templates for the application
index.html: The main landing page
register.html: The registration form page
search.html: The search results page
edit.html: The edit user information page
print_qr.html: The print QR code page
static: Directory containing static assets for the application
css: Directory containing CSS stylesheets
index.css: Styles for the main landing page
search.css: Styles for the search results page
styles.css: General styles for the application
js: Directory containing JavaScript files
scripts.js: JavaScript code for the application
README.md: This file
License
This project is licensed under the MIT License. See LICENSE for details.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.