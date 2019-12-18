# How To Install?

Create a .env file with contents
```env
FLASK_APP=run
FLASK_ENV=development
SQLALCHEMY_ECHO=False
SQLALCHEMY_TRACK_MODIFICATIONS=True
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/everphone
```

Run following command to create a virtualenv and install the dependencies.

```bash
sudo apt install python3-pip
sudo pip3 install pipenv
pipenv shell --python 3.6
pipenv install --ignore-pipfile
```

Upgrade db tables using,

```bash
python migrate.py db upgrade
```

Run the app using,

```bash
python run.py
```

Now, we can add employee and gift data to the postgresql database, using scripts.
* To add employees, run the following command in project root directory.

```bash
export PYTHONPATH=.
python scripts/add_employees.py
```
* And to add gifts, run
```bash
export PYTHONPATH=.
python scripts/add_gifts.py
```

Once we have the data in database, we can start assigning the gifts to employees
* Method: POST
* API endpoint : http://127.0.0.1:5000/api/employee/47/assign_gift
* Body: N/A
* Response : `{
    "status": "success",
    "data": {
        "gift": "spotify voucher"
    }
}`

![Alt text](screenshots/assign_gift.png?raw=true "Assign Gift")
