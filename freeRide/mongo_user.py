from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import request, jsonify, Blueprint, redirect, current_app, url_for
from flask_login import current_user, login_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from .mongo import ride_request
from .mongo_driver import driver_rides


mongo_user = Blueprint('mongo_user', __name__)

uri = "mongodb+srv://RaunakBhansali:951203@cluster0.reeyyqp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['acoount']
rides = db['rides']
payment = db['payment']
user = db['user']


@mongo_user.route('/add_ride/<request_id>/<car_type>', methods=['POST', 'GET'])
@login_required
def add_ride(request_id, car_type):

    request_id = int(request_id)
    driver_doc = driver_rides.find_one({'ride_details.request_id': request_id})
    if driver_doc:
        driver_id = driver_doc['driver_id']
    result_doc = ride_request.find_one({'car_type': car_type, 'ride_details.request_id' : request_id})

    if result_doc:
        result = result_doc['ride_details'][0]
    else: 
        return jsonify({'message': 'ride not found'}), 404

    user_id = current_user.id
    ride_details = {
            'request_id': request_id,
            'driver_id': driver_id,
            'pickup': result['pickup'],
            'drop': result['drop'],
            'pickup_time': result['pickup_time'],
            'payment': result['payment_type'],
            'car_type': car_type,
            'amount': result['ride_fare'],
            'timestamp': datetime.utcnow()
        }

    rides_doc = rides.find_one({'user_id' : user_id})

    if rides_doc:
        result = rides.update_one(
            {'user_id' : user_id},
            {'$push' : {'ride_details' : ride_details}}
        )
        if result.modified_count == 1:
            return redirect(url_for('views_user.user_ongoing_ride', request_id = request_id, car_type = car_type))
        else:
            return jsonify({'message': 'Failed to add ride'}), 500

    else:
        new_ride = {
            'user_id': user_id,
            'ride_details': [ride_details],
        }

        result = rides.insert_one(new_ride)
        if result.inserted_id:
            return redirect(url_for('views_user.user_ongoing_ride', request_id = request_id))
        else:
            return jsonify({'message': 'Failed to add ride'}), 500

# Route for adding payment details
@mongo_user.route('/add_payment', methods=['POST'])
@login_required
def add_payment():
    data = request.json
    user_id = current_user.id
    payment_details = {
        'payment_method': data.get('payment_method'),  # Assuming payment method is provided in the request JSON
        'payment_details': data.get('payment_details'),  # Assuming payment details are provided in the request JSON
        'timestamp': datetime.utcnow()
    }

    payment_doc = payment.find_one({'user_id' : user_id})

    if payment_doc:
        result = payment.update_one(
            {'user_id' : user_id},
            {'$push' : {'payment_details' : payment_details}}
        )
        
        if result.modified_count == 1:
            return jsonify({'message': 'successfully added payment details'}), 200
        else:
            return jsonify({'message': 'Failed to add payment details'}), 500

    else:
        new_payment = {
            'user_id': user_id,
            'payment_details': [payment_details],
        }

        result = payment.insert_one(new_payment)
        if result.inserted_id:
            return jsonify({'message': 'successfully added payment details'}), 200
        else:
            return jsonify({'message': 'Failed to add payment details'}), 500

# Route for updating user details
@mongo_user.route('/add_user', methods=['POST'])
@login_required
def add_user():
    user_id = current_user.id

    profile_image = request.files['profile_image']
    if profile_image:
        profile_image_filename = secure_filename(profile_image.filename)
        profile_image.save(os.path.join(current_app.config['DRIVER_PROFILE'], profile_image_filename))
    else:
        profile_image_filename = "default_profile.avif"

    user_details = {
            'email': request.form['email'],
            'display_name': request.form['display_name'],
            'phone': request.form['phone'],
            'profile_image' : profile_image_filename,
            'timestamp': datetime.utcnow()
        }

    user_doc = user.find_one({'user_id' : user_id})

    if user_doc:
        user.update_one(
            {'user_id' : user_id},
            {'$push' : {'user_details' : user_details}}
        )

    else:
        new_driver = {
            'user_id': user_id,
            'user_details': [user_details],
        }

        result = user.insert_one(new_driver)
    if result.inserted_id:
        return redirect(url_for('views_user.homepage'))
    else:
        return jsonify({'message': 'Failed to add driver'}), 500
    
