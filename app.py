from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm


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
        session['username'] = new_user.username

        return redirect(f"/users/{new_user.username}")
    
    else: return redirect("users/register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Generates login form to handle logins"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!", "success")
            session ['username'] = user.username
            return redirect(f"/users/{user.username}")
        
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)
            
    return render_template("users/login.html", form=form)
    

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

@app.route("/user/<username>")
def user_page(username):
    """logged in user page"""
    if 'username' not in session or username != session['username']:
        flash(f"Please login.")

    user = User.query.get(username)
    
    return render_template("users/show.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes user and redirects to register"""
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop(username)

    return redirect("/register")

@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def new_feedback(username):
    if 'username' not in session or username != session['username']:
        flash(f"Please login.")
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content= form.content.data

        feedback= Feedback(title = title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/new.html", form=form)
    
@app.route("/feedback/<feedback_id>/update")
def update_feedback(feedback_id):
    """Displays the update feedback form and submits the update"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        flash(f"Please login.")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<feedback-id>/delete")
def delete_feedback(feedback_id):
    """Deletes feedback """
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        flash(f"Please login.")

    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback Removed")
        return redirect("/users/{feedback.username}")
    flash("You don't have permission to do that!")
    return redirect("/users/{feedback.username}")


