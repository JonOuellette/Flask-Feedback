from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    return redirect("/register")

@app.route("/register", methods = ['GET', 'POST'])
def register_user():
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
    
        new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/secret")
    
    else: return render_template("users/register.html", form=form)


@app.route("/secret")
def secret_page():
    return render_template("secret.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Generates login form to handle logins"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            return redirect("/secret")
        
        else:
            form.username.errors = ["Invalid username/password."]
            
    
    return render_template("users/login.html", form=form)