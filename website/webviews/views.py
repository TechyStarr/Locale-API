# contain all the routes
import secrets
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.models.users import User
from website.utils.utils import db
from website.models.data import Region, State, Lga
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


views = Blueprint("views", __name__)


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



@views.route("/")
@cache.cached(timeout=60) # Cache the response for 60 seconds
@limiter.limit("100 per minute")
def index():
    # regions = Region.query.all()
    return render_template("index.html", current_user=current_user)




@views.route("/q", methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        q = request.form.get('q')
        if q:
            results = State.query.join(Region).filter(
                db.or_(
                    State.name.ilike(f'%{q}%'),
                    State.capital.ilike(f'%{q}%'),
                    # State.lgas.ilike(f'%{q}%'),
                    Lga.name.ilike(f'%{q}%'),
                    Region.name.ilike(f'%{q}%')  # Include region name in the search
                )
            ).all()
            return render_template("search.html", results=results)
        else:
            return redirect(url_for('views.index'))
    else:
        return redirect(url_for('views.index'))
    


@views.route("/dev")
# @login_required
def dev():
    return render_template("dev.html", current_user=current_user)


def api_key():
    api_key = secrets.token_hex(16)
    return api_key


@views.route("/generate-api-key")
# @login_required
def generate_api_key():
    if request.method == "GET":
        user = User.query.filter_by(email=current_user.email).first()
        user.api_key()
        try:
            user.save()
            flash( "Your api key is {}".format(user.api_key), category="success")
            flash("API Key generated successfully", category="success")
            return redirect(url_for("views.dev"))
        except:
            flash("API Key generation failed", category="danger")
            return redirect(url_for("views.dev"))
    else:
        flash("You're not authorized to do this", category="danger")
        return redirect(url_for("views.dev"))
