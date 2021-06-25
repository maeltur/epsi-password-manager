import base64
from hashlib import sha512
import MySQLdb
from flask import Blueprint, request, render_template, session, url_for, current_app,app
from flask_login import login_user, login_required, logout_user
from flask_mysqldb import MySQL

from passwordmanager import credentialsmsql

auth = Blueprint('auth', __name__)
# current_app.config = {'MYSQL_HOST': '192.168.1.30', 'MYSQL_USER': credentialsmsql.user,
#                      'MYSQL_PASSWORD': credentialsmsql.password, 'MYSQL_DB': 'passmanager'}
with app.app_context():
    mysql = MySQL(current_app)
    con = mysql.connection()
    cursor = con.cursor(MySQLdb.cursors.DictCursor)


# ------------------- LOGIN --------------------
@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if 'email' in request.form and 'password' in request.form:

        # Create variables for easy access
        mail = request.form['email']
        password = request.form['password']
        h = sha512()
        password = base64.b64decode(password)
        h.update(password)
        password = h.hexdigest()
        cursor.execute('SELECT * FROM Compte WHERE email = %s AND password = %s', (mail, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        if not account:
            output = 'Incorrect mail/password!'
        else:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['idCompte'] = account['idCompte']
            session['email'] = account['email']
            user = {'loggedin': True, 'idCompte': account['idCompte'], 'email': account['email']}
            login_user(user)
            # Redirect to home page
            output = 'Logged in successfully!'
            # Account doesnt exist or username/password incorrect
    else:
        output = "Please provide mail and password"
    return output


# ------------------- SIGNUP --------------------

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if 'nom' in request.form and 'password' in request.form and 'prenom' in request.form and 'email' in request.form:
        # Create variables for easy access
        nom = request.form['nom']
        prenom = request.form['prenom']
        password = request.form['password']
        h = sha512()
        password = base64.b64decode(password)
        h.update(password)
        password = h.hexdigest()
        email = request.form['email']
        try:
            cursor.execute("INSERT INTO `Compte` (`nom`, `prenom`, `email`, `password`) VALUES (%s, %s, %s, %s)",
                           (nom, prenom, email, password))
            con.commit()
            print("Your account have been created")
        except Exception as exception:
            msg = "Your account couldn't be added : " + str(exception)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return msg


# ----------------------- LOGOUT -------------------
@auth.route('/logout')
@login_required
def logout():
    # Remove session data, this will log the user out
    logout_user()
    session.pop('loggedin', None)
    session.pop('idCompte', None)
    session.pop('email', None)
    # Redirect to login page
    return render_template(url_for('main.index'))
