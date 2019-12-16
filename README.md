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
flask run
```
