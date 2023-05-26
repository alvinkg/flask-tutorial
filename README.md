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
