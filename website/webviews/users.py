from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, jsonify
# from flask_smorest import Blueprint, abort
from website.models.users import User
from website.utils.utils import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

auth = Blueprint("Users", __name__)

app = Flask(__name__)


# cache response for 60 seconds
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# rate limit of 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )





# signup route
@auth.route('/signup', methods = ['GET', 'POST'])
@cache.cached(timeout=60) # Cache the response for 60 seconds

def register():
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')

		password_hash = generate_password_hash(password)
		email_exists = User.query.filter_by(email=email).first()
		if email_exists:
			flash('This mail already exists!', category='error')
		# elif password != confirm_password:
		# 	flash('Password does not match.', category='error')
		elif len(password) < 8:
			flash('Password is too short.', category='error')
		elif len(email) < 5:
			flash('Invalid email.', category='error')
		else:
			new_user = User(username = username, email = email, password = password_hash)
			db.session.add(new_user)
			db.session.commit()
			flash('Your account has been created!')
			login_user(new_user, remember=True)

			return redirect(url_for('views.index'))

	return render_template('register.html')








@auth.route("/login", methods=['GET', 'POST'])
@cache.cached(timeout=60) # Cache the response for 60 seconds
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password_hash = request.form.get("password")
        print(email, password_hash)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password_hash):
                flash(f"Good to have you back, {user.username}", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash("Incorrect password!", category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")




@auth.route("/contact", methods=['GET', 'POST'])
@cache.cached(timeout=60) # Cache the response for 60 seconds
def contact():
    if request.method == 'POST':
            flash('We appreciate the feedback, be on the lookout for our response', category='success')
    return render_template("contact.html", current_user=current_user)


@auth.route('/logout')
@login_required
@cache.cached(timeout=60) # Cache the response for 60 seconds
def logout():
	logout_user()
	flash('Logout successful')
	return redirect(url_for('aven.index'))













