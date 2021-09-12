# Assignment

## Execution Steps

1. Install <b>git</b> on the system.
2. Open shell/command prompt and run following command to clone the project:
    <br>`git clone https://github.com/Rashiddev/assignment.git`
3. Make sure <b>python3</b> and <b>pip3</b> are installed on the system.
4. Once inside the project's root directory, install requirements using the following command:
    <br>` pip install -r ./requirements/local.txt`
5. Run this command inside the project directory to start the server:
    <br>`python3 manage.py runserver 8000`
6. Following URL will open swagger UI from where all the project APIs can be accessed:
    <br>http://127.0.0.1:8000/api/schema/swagger/
7. All APIs are public and can be accessed without authentication except Car Create API.
   <br> To access Car Creat API, user can authorize using following credentials from Swagger UI:
   - username: <b>admin</b>
   - password: <b>admin@123$</b>

### Data import from excel
There is a management command available that can be used to import data in a fresh db.
CSV files should be placed in <b>data</b> directory inside project root for this command
to work.
<br>`python manage.py import_cars_data`

- <b>Note</b>
  <br>The command currently skips invalid records. It could be further improved to save logs for failed records that can corrected and imported again to avoid data lost.
  

## Tests
Following command can be used to run test cases:
<br>`python manage.py test`


