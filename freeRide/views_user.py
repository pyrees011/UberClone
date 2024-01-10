from flask import Blueprint, redirect, render_template, url_for, current_app, flash
from flask_login import login_user, logout_user, login_required, current_user
from .mongo_user import rides
from .mongo import ride_request
from .mongo_driver import driver

views_user = Blueprint("views_user", __name__, template_folder='templates/views/views_user')

@views_user.route('/')
def webpage():
    if current_user.is_authenticated:
        return redirect(url_for('views_user.homepage'))
    return render_template('webpage.html')

@views_user.route('/homepage', methods=['GET'])
@login_required
def homepage():
    current_app.logger.info('i am redirected')
    return render_template('homepage.html')

@views_user.route('/ride_webpage', methods=['GET'])
def ride_webpage():
    return render_template('ride_webpage.html')

@views_user.route('/mytrip', methods=['GET', 'POST'])
@login_required
def mytrip():
    return render_template('mytrip.html')

@views_user.route('/payment', methods=['GET'])
@login_required
def payment():
    return render_template('payment.html')

@views_user.route('/profile_settings', methods=['GET'])
@login_required
def profile_settings():
    return render_template('profile_settings.html')

@views_user.route('/tax_profile', methods=['GET'])
@login_required
def tax_profile():
    return render_template('tax_profile.html')

@views_user.route('/user_info', methods=['GET'])
@login_required
def user_info():
    return render_template('user_info.html')

@views_user.route('/user_ongoing_ride/<request_id>/<car_type>', methods=['GET'])
@login_required
def user_ongoing_ride(request_id, car_type):

    request_id = int(request_id)

    ride_doc = ride_request.find_one({'car_type': car_type, 'ride_details.request_id' : request_id})
    if ride_doc['ride_details'][0]['status'] == "finished":
        return redirect(url_for('views_user.homepage'))

    result_doc = rides.find_one({'user_id': current_user.id, 'ride_details.request_id' : request_id})
    if result_doc:
        ride_details = result_doc['ride_details'][0]
        driver_id = int(result_doc['ride_details'][0]['driver_id'])

        driver_doc = driver.find_one({'driver_id': driver_id})
        driver_info = driver_doc['driver_details'][0]


    return render_template('user_ongoing_ride.html', ride_details = ride_details, driver_info = driver_info)

@views_user.route('/waiting_page/<request_id>/<car_type>', methods=['GET'])
@login_required
def waiting_page(request_id,car_type):

    request_id = int(request_id)
    result_doc = ride_request.find_one({'car_type': car_type, 'ride_details.request_id' : request_id})

    if result_doc:
        if result_doc['ride_details'][0]['status'] == "accepted":
            return redirect(url_for('mongo_user.add_ride', request_id = request_id, car_type = car_type))
    return render_template('waiting_page.html')