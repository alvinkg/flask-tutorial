from flask import Flask, g, session, redirect, abort, url_for, request, render_template
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key='key'

    # gen good secret keys
    # >>> import secrets
    # >>> print(secrets.token_hex())
    # 34ed0ded2daa847961058c04ab88b4069a6155cb771094e22d32d7aaed01c333

    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    
    # initialize the app with the extension
    db.init_app(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True, nullable=False)
        email = db.Column(db.String)

        def __init__(self, username, email):
            self.username = username
            self.email = email

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
    
    # only after models defined and imported
    with app.app_context():
        db.create_all()
        
    return app