from flask import Blueprint, redirect, render_template, url_for, current_app, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Driver, SignupForm_user, SignupForm_driver, LoginForm, googleUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json

auth = Blueprint("auth", __name__, template_folder='templates/auth')
google_client_id = os.environ.get("GOOGLE_CLIENT_ID", None)
google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", None)

google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(google_client_id)

@auth.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = SignupForm_user()

    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')
        display_name = form.display_name.data

        new_user = User(username=username, email=email, password=password, display_name=display_name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views_user.user_info'))


    return render_template('register_user.html', form=form)


@auth.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    form = SignupForm_driver()

    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')
        display_name = form.display_name.data
        vehicle_type = form.vehicle_type.data

        new_driver = Driver(username=username, email=email, password=password, display_name=display_name, vehicle_type=vehicle_type)
        db.session.add(new_driver)
        db.session.commit()
        login_user(new_driver, remember=True)
        return redirect(url_for('views_driver.driver_info'))


    return render_template('register_driver.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        driver = Driver.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views_user.homepage'))
            else:
                flash('Incorrect password, try again.', category='danger')
        elif driver:
            # if check_password_hash(driver.password, password):
            if check_password_hash(driver.password,password):
                flash('Logged in successfully!', category='success')
                login_user(driver, remember=True)
                return redirect(url_for('views_driver.driver_homepage'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Username does not exist.', category='danger')

    return render_template('login.html', form=form)

@auth.route('/login/google')
def google_login():
    google_provider_cfg = requests.get(google_discovery_url).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    current_app.logger.info(request.base_url)

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["email"],
    )
    return redirect(request_uri)

@auth.route("/login/google/callback")
def callback():
    # Get the authorization code from the callback URL
    code = request.args.get("code")

    google_provider_cfg = requests.get(google_discovery_url).json()
    # Prepare the token request
    token_url, headers, body = client.prepare_token_request(
        google_provider_cfg["token_endpoint"],
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    # Send the token request and get the token response
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret)
    )

    # Parse the token response
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get the user info from the userinfo endpoint
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Parse the user info response
    userinfo = userinfo_response.json()

    # Check if the user already exists in the database
    google_user = googleUser.query.filter_by(email=userinfo["email"]).first()

    if google_user:
        # User already exists, log them in
        login_user(google_user, remember=True)
        flash('Logged in successfully!', category='success')
        return redirect(url_for('views_user.homepage'))
    else:
        # User does not exist, create a new user
        new_google_user = googleUser(
            email=userinfo["email"],
        )
        db.session.add(new_google_user)
        db.session.commit()

        # Log in the new user
        login_user(new_google_user, remember=True)
        flash('Logged in successfully!', category='success')
        return redirect(url_for('views_user.homepage'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views_user.webpage'))