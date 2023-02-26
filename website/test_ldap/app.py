from flask import Flask
from flask_ldap3_login import LDAP3LoginManager

app = Flask(__name__)

# Configure the LDAP login manager
ldap_manager = LDAP3LoginManager(app)

# Set the LDAP server details
ldap_manager.init_config(
    ldap3_server_uri='ldap://messenger.com',
    base_dn='dc=messenger,dc=com',
    user_rdn_attribute='mail',
    user_password_attribute='userPassword'
)

# Define the LDAP login and logout routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check for empty or None values
        if not form.username.data or not form.password.data:
            flash('Invalid username or password')
            return render_template('login.html', form=form)
        # Attempt to authenticate the user
        user = ldap_manager.authenticate(form.username.data, form.password.data)
        if user:
            # Login successful
            login_user(user)
            flash('You have been logged in')
            return redirect(url_for('protected'))
        else:
            # Login failed
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

# Require LDAP authentication for the /protected route
@app.route('/protected')
@ldap_manager.login_required
def protected():
    return 'You are logged in!'
