# Assignment

## Docker setup
### Clone your repo
    $ git clone https://github.com/Rashiddev/assignment.git

### Make sure docker is installed on your system and run following commands inside your project directory:

    $ docker-compose build
    $ docker-compose up

### Create an admin user
    $ docker-compose exec web python manage.py createsuperuser

### Interact with APIs on this URL:
    $ http://127.0.0.1:8000/api/schema/swagger/

### Run tests
    $ docker-compose exec web python manage.py test


## Development Steps

1. Install <b>git</b> on the system.
2. Open shell/command prompt and run following command to clone the project:


    $ git clone https://github.com/Rashiddev/assignment.git


3. Make sure <b>python3</b> and <b>pip3</b> are installed on the system.
4. Once inside the project's root directory, install requirements using the following command:
    <br>Note: It's recommended to create a virtual environment and install requirements there.

    
    $ pip install -r ./requirements/local.txt

5. Run this command inside the project directory to start the server:
    

    $ python3 manage.py runserver 8000

6. Following URL will open swagger UI from where all the project APIs can be accessed:


    http://127.0.0.1:8000/api/schema/swagger/

7. All APIs are public and can be accessed without authentication except Car Create API.
   <br> To access Car Creat API, user can authorize using following credentials from Swagger UI:
   
    
    username: admin
    password: admin@123$

### Data import from excel
There is a management command available that can be used to import data in a fresh db.
CSV files should be placed in <b>data</b> directory inside project root for this command
to work.


    $ python manage.py import_cars_data

- <b>Note</b>
  <br>The command currently skips invalid records. It could be further improved to save logs for failed records that can corrected and imported again to avoid data lost.
  

## Tests
Following command can be used to run test cases:


    $ python manage.py test


