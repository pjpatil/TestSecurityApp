from flask import Flask, request, redirect, url_for, render_template, flash
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = '9f2a1b8c4d6e7f0123456789abcdef01'

# LDAP Config - using your IP as domain
app.config['LDAP_HOST'] = 'ldap'  # Docker internal name
app.config['LDAP_BASE_DN'] = 'dc=163,dc=53,dc=203,dc=3'
app.config['LDAP_USER_DN'] = 'ou=People'
app.config['LDAP_GROUP_DN'] = 'ou=Groups'
app.config['LDAP_USER_RDN_ATTR'] = 'uid'
app.config['LDAP_BIND_USER_DN'] = 'cn=admin,dc=163,dc=53,dc=203,dc=3'
app.config['LDAP_BIND_USER_PASSWORD'] = 'pankaj4433'

ldap_manager = LDAP3LoginManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
    return render_template("dashboard.html", username=current_user.name)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
