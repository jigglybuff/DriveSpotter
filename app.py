from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_httpauth import HTTPBasicAuth
from flask import render_template, request, redirect, url_for
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

from flask_security.forms import RegisterForm
from wtforms import StringField, TextAreaField, SubmitField, TextField
from wtforms.validators import InputRequired, Email

from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
auth = HTTPBasicAuth()
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:testtest@localhost/Users'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.debug = True
db = SQLAlchemy(app)


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    first_Name = db.Column(db.String(255))
    last_Name = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class ExtendedRegisterForm(RegisterForm):
    first_Name = TextField('First Name', [InputRequired()])
    last_Name = TextField('Last Name', [InputRequired()])

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

@app.route('/')
@login_required
def index():
	myUser = User.query.all()
	return render_template('add_user.html', myUser=myUser)

@app.route('/profile/<email>')

def profile(email):
	user = User.query.filter_by(email=email).first()
	return render_template('profile.html', user=user)

@app.route('/post_user', methods=['POST'])
@login_required
def post_user():
	user = User(request.form['email'], request.form['first_Name'], request.form['last_Name'], request.form['password'])
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run()