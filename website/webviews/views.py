# contain all the routes
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.models.users import User
from website.utils.utils import db
from website.models.data import Region, State, Lga



views = Blueprint("views", __name__)


# @views.route("/")
# def index():

#     return render_template("index.html", current_user=current_user)


@views.route("/")
def index():
    # regions = Region.query.all()
    return render_template("index.html")


# @views.route("/q", methods=['GET', 'POST'])
# def q():
#     if request.method == 'POST':
#         q = request.form.get('q')
#         if q:
#             lgas = Lga.query.filter(Lga.name.contains(q)).all()
#         else:
#             lgas = Lga.query.all()
#         return render_template("index.html", lgas=lgas)

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
            return render_template("index.html", results=results)
        else:
            return redirect(url_for('views.index'))
    else:
        return redirect(url_for('views.index'))
    


@views.route("/dev")
def dev():
    return render_template("dev.html", current_user=current_user)







# @views.route("/q", methods=['GET', 'POST'])
# def q():
#     keyword = request.args.get('keyword')
#     if keyword:
#         results = State.query.join(Region).filter(
#             db.or_(
#                 State.name.ilike(f'%{keyword}%'),
#                 State.capital.ilike(f'%{keyword}%'),
#                 # State.lgas.ilike(f'%{keyword}%'),
#                 Lga.name.ilike(f'%{keyword}%'),
#                 Region.name.ilike(f'%{keyword}%')  # Include region name in the search
#             )
#         ).all()



#         # Serialize the search results
#         data = [state.serialize() for state in results]
#         return jsonify(data), 200
#     else:
#         return {'message': 'No keyword provided'}, 400
    


@views.route("/about")
def about():
    return render_template("about.html", current_user=current_user)












# def get_states(region_id):
#     states = State.query.filter_by(region_id=region_id).all()
#     return states

# def get_lgas(state_id):
#     lgas = Lga.query.filter_by(state_id=state_id).all()
#     return lgas

# @views.route("/states/<int:region_id>")
# def states(region_id):
#     states = get_states(region_id)
#     context = {
#         'states': states
#     }
#     return render_template("states.html", user=current_user, context=context)

# @views.route("/lgas/<int:state_id>")
# def search(self):
#     q = request.args.get('q')
#     if q:
#         lgas = Lga.query.filter(Lga.name.contains(q)).all()
#     else:
#         lgas = Lga.query.all()
#     return render_template("index.html", lgas=lgas)




# # about route displays info about the page
# @views.route('/about')
# def about():
# 	return render_template('about.html')


# @views.route("/contact", methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         flash('We appreciate the feedback, be on the lookout for our response',
#                 category='success')
#     return render_template("contact.html", current_user=current_user)



