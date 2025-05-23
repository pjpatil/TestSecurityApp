# app.py
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
# app.secret_key = 'your-secret'
app.secret_key = '9f2a1b8c4d6e7f0123456789abcdef01'

# LDAP Config

app.config['LDAP_HOST'] = '127.0.0.1'
app.config['LDAP_BASE_DN'] = 'dc=vector-india,dc=in'
app.config['LDAP_USER_DN'] = 'ou=People'
app.config['LDAP_GROUP_DN'] = 'ou=Groups'
app.config['LDAP_USER_RDN_ATTR'] = 'uid'
app.config['LDAP_BIND_USER_DN'] = 'cn=admin,dc=vector-india,dc=in'
app.config['LDAP_BIND_USER_PASSWORD'] = 'pankaj4433'

ldap_manager = LDAP3LoginManager(app)

class User(UserMixin):
    def __init__(self, dn, username):
        self.id = dn
        self.name = username

users = {}

@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username)
    users[dn] = user
    return user

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("username:",username)
        print("password:",password)

        response = ldap_manager.authenticate(username, password)

        if response.status:
            login_user(response.user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # return f"Welcome {users.get(current_user.id).name}!"
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
