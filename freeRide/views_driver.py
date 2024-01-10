from flask import Blueprint, redirect, render_template, url_for, current_app, flash
from flask_login import login_user, logout_user, login_required, current_user
from .mongo import ride_request
from .mongo_driver import driver, driver_rides
from .mongo_user import user

views_driver = Blueprint("views_driver", __name__, template_folder='templates/views/views_driver')

@views_driver.route('/')
def webpage():
    if current_user.is_authenticated:
        return redirect(url_for('views_driver.driver_homepage'))
    return render_template('webpage.html')

@views_driver.route('/driver_home')
@login_required
def driver_homepage():

    user_doc = driver.find_one({'driver_id' : current_user.id})
    car_type = user_doc['driver_details'][0]['car_type']

    request_doc = ride_request.find_one({'car_type' : car_type})
    if request_doc['ride_details'][0]['status'] == 'requested':
        ride_details = request_doc['ride_details']
    else:
        ride_details = {}
    # current_app.logger.info(request_doc)

    return render_template('driver_homepage.html', ride_details = ride_details, car_type = car_type)

@views_driver.route('/driver_info')
@login_required
def driver_info():
    return render_template('driver_info.html')

@views_driver.route('/ride_webpage')
def ride_webpage():
    return render_template('ride_webpage.html')

@views_driver.route('/driver_mytrip')
@login_required
def driver_mytrip():
    return render_template('driver_mytrip.html')

@views_driver.route('/driver_payment')
@login_required
def driver_payment():
    return render_template('driver_payment.html')

@views_driver.route('/driver_profile_settings')
@login_required
def driver_profile_settings():
    return render_template('driver_profile_settings.html')

@views_driver.route('/driver_tax_profile')
@login_required
def driver_tax_profile():
    return render_template('driver_tax_profile.html')

@views_driver.route('driver_ongoing_ride/<request_id>/<car_type>')
@login_required
def driver_ongoing_ride(request_id, car_type):

    request_id = int(request_id)

    ride_doc = ride_request.find_one({'car_type': car_type, 'ride_details.request_id' : request_id})
    if ride_doc['ride_details'][0]['status'] == "finished":
        return redirect(url_for('views_driver.driver_homepage'))

    user_doc = driver_rides.find_one({'driver_id' : current_user.id, 'ride_details.request_id' : request_id})

    ride_details = user_doc['ride_details'][0]
    user_id = ride_details['user_id']

    user_doc = user.find_one({ 'user_id': user_id })
    user_info = user_doc['user_details'][0]
    current_app.logger.info(user_info)

    current_app.logger.info(user_id)
    return render_template('driver_ongoing_ride.html', ride_details = ride_details, user_info = user_info)