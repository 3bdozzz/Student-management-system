Student Management System
This is a Python project that connects to a MySQL database to manage student data.

Features
Add, update, and view student records
Connects to a MySQL database
Secure database credentials using .env file
To run the project, make sure you have Python and MySQL installed, and that the database schema matches the tables used in the code. Before running, install all dependencies listed in the requirements.txt file using the command pip install -r requirements.txt.

Next, create a file named .env in the main project folder and add your database credentials inside it. For example:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=booking

The .env file is already listed in .gitignore, so it will not be uploaded to GitHub for security reasons. Once the .env file is ready, you can run the system by executing the main Python file. The program will automatically read database credentials from the .env file.

This project was developed by Abdulrahman Omar as part of a university assignment to demonstrate full system integration and secure environment configuration.
