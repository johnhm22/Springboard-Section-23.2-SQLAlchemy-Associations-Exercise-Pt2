"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_create_user_form():
    """Show new user form"""
    return render_template('/new_user_form.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Create a new user in db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """ show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show new user form"""
    user = User.query.get(user_id)
    return render_template('/edit_user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Update a user in db
    uses a sql query to first find the user from id
    assigns details from form to each of the columns
    adds user with updated details to session
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    updated_user = User.query.get(user_id)
  
    updated_user.first_name = first_name
    updated_user.last_name = last_name
    updated_user.image_url = image_url
    db.session.add(updated_user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ delete a single user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")


