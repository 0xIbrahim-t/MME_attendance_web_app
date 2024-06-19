# MME attendance web app

## Set Up Your Environment
1. apt-get install python3 mysql-server
2. pip install Flask mysql-connector-python werkzeug gunicorn

## Set up the database for attendance app
1. enter the users name, rollnumber and password for login in students.txt and in professors.txt
> mysql -u root -p
>> CREATE DATABASE attendance_app;
>> 
>> CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'securepassword';
>> 
>> GRANT ALL PRIVILEGES ON attendance_app.* TO 'attendance_user'@'localhost';
>> 
>> FLUSH PRIVILEGES;
>> 
>> EXIT;
> python3 init_db.py
>
> python3 load_users.py

## Run the application
1. first run locally to check if it works.
> flask run
2. Set up Gunicorn to run the Flask application in production
> gunicorn -w 4 -b 127.0.0.1:5000 app:app
and the app will run on the port 5000

