# Flask Tutorial for 2023

This was my flask tutorial to resolve app-context issues that were preventing me from completing the flask tutorial by 'Tech with Tim' that spanned more than ten bite sized videos.
When I got to tutorial 8 I could not get the sqlite database to work try as I may even after changing my code to accomodate the suggestions in stack overflow website.
I next tried the tutorial inside the flask-sqlalchemy site.  That did not work either.
Finally I had no choice but to leverage a previous package I build that worked that was for the usage of blueprints in flask.
I am still curious to know what went wrong but for now this repo documents how with limited modularity I was able to get my sqlite database to work.

## Choose python version and setup virtual environment

I chose python3 version 3.9.2.
I use pyenv to manage my python versions.
I use virtualenv as it allows me to make a directory local to a virtual environment so that I don't need to remember to activate the environment when working inside.  However since I use VS Code I still need to setup the correct virtual environment to match my command line interface.

```bash
% pyenv 3.9.2 virtualenv flask-tutorial
% pyenv local flask-tutorial
% pyenv activate flask-tutorial
```

The last command is needed when virtualenv is buggy and needs prompting!

## Install Flask and flask_sqlalchemy

Install the packages inside the command line interface.

```bash
% pip install flask
% pip install flask-sqlalchemy
```

Alternatively we can add them to a requirements.txt file and run the file.  This keeps the file free of clutter as the sub-packages are not included.
So type the following inside your requirments.txt file.

```bash
Flask==2.3.2
Flask-SQLAlchemy==3.0.3
```

The above was done using the below commands and trimming out the extra packages that are not required when using github.

```bash
% pip freeze > requirements.txt
```

## create a folder for your package

In this example I create a folder 'server' and added a file __init__.py inside to make it a python package.  This file has most of my code, including my models and views.  In another tutorial on Blueprints, these are parcelled into different directories for tidiness and ease of sharing as an application.
The code you see inside reflects my efforts to work through the flask-sqlalchemy tutorial found here in this [link](https://flask-docs.readthedocs.io/en/latest/).

## Add __init__.py to your package

```bash
% touch __init__.py
```

## Import Flask, SQLAlchemy into __init__.py

```bash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
```

## Add instance of SQLAlchemy

```bash
db = SQLAlchemy()
```

## Add method 'create_app' & instance of Flask

```bash
def create_app():
    app = Flask(__name__)
```

## Generate a secret key and add to 'app' the Flask app

Generate your secret key using your python prompt.

```bash
% python
>>> import secrets
>>> print(secrets.token_hex())
34ed0ded2daa847961058c04ab88b4069a6155cb771094e22d32d7aaed01c333
```

```bash
def create_app():
    app = Flask(__name__)
    app.secret_key = '34ed0ded2daa847961058c04ab88b4069a6155cb771094e22d32d7aaed01c333'
```

## Config the path to the database of choice

```bash
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
```

## Initiatize the database using the Flask app

```bash
db.init_app(app)
```

## Add tables using models or classes

```bash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

    def __init__(self, username, email):
        self.username = username
        self.email = email
```

## Add views

```bash
        @app.route("/users")
        def user_list():
            users = db.session.execute(db.select(User).order_by(User.username)).scalars()
            return render_template("user/list.html", users=users)

        @app.route("/users/create", methods=["GET", "POST"])
        def user_create():
            if request.method == "POST":
                user = User(
                    username=request.form["username"],
                    email=request.form["email"],
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("user_detail", id=user.id))

            return render_template("user/create.html")

        @app.route("/user/<int:id>")
        def user_detail(id):
            user = db.get_or_404(User, id)
            print(user.username, user.email)
            return render_template("user/detail.html", user=user)

        @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
        def user_delete(id):
            user = db.get_or_404(User, id)

            if request.method == "POST":
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for("user_list"))

            return render_template("user/delete.html", user=user)
```

## Once models are defined and imported add context

```bash
with app.app_context():
    db.create_all()

return app
```

## Add a main python file to import and call the 'create_app'

```bash
from server import create_app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
```

## Add the html files to the templates directory

Add as required.
