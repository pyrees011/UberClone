from flask import Blueprint, request, jsonify, current_app, redirect, url_for
from flask_login import current_user
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from .mongo import ride_request

uri = "mongodb+srv://RaunakBhansali:951203@cluster0.reeyyqp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

mongo_driver = Blueprint('mongo_driver', __name__)

db = client['acoount']
driver_rides = db['driver_rides']
driver_payment = db['driver_payment']
driver = db['driver']

@mongo_driver.route("/add_driver_details", methods=['POST'])
def add_driver_details():
    if request.method == "POST":
        driver_id = current_user.id

        license_image = request.files['license_image']
        if license_image:
            license_image_filename = secure_filename(license_image.filename)
            license_image.save(os.path.join(current_app.config['DRIVER_PROFILE'], license_image_filename))

        profile_image = request.files['profile_image']
        if profile_image:
            profile_image_filename = secure_filename(profile_image.filename)
            profile_image.save(os.path.join(current_app.config['DRIVER_PROFILE'], profile_image_filename))
        else:
            profile_image_filename = "default_profile.avif"

        driver_details = {
                'display_name': current_user.display_name,
                'car_type': request.form['car_type'],
                'plates': request.form['plates'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'license_image' : license_image_filename,
                'profile_image' : profile_image_filename,
                'timestamp': datetime.utcnow()
            }

        driver_doc = driver.find_one({'driver_id' : driver_id})

        if driver_doc:
            driver.update_one(
                {'driver_id' : driver_id},
                {'$push' : {'driver_details' : driver_details}}
            )

        else:
            new_driver = {
                'driver_id': driver_id,
                'driver_details': [driver_details],
            }

            result = driver.insert_one(new_driver)
        if result.inserted_id or result.modified_count == 1:
            return redirect(url_for('views_driver.driver_homepage'))
        else:
            return jsonify({'message': 'Failed to add driver'}), 500
        

@mongo_driver.route("/add_driver_ride", methods=['POST'])
def add_driver_ride():
    if request.method == "POST":
        driver_id = current_user.id
        data = request.json

        car_type = data.get('car_type')
        request_id = int(data.get('request_id'))

        result = ride_request.find_one(
            {'car_type': car_type, 'ride_details.request_id': request_id}
        )

        ride_options = result['ride_details'][0]

        ride_details = {
                'request_id': request_id,
                'pickup': ride_options['pickup'],
                'drop': ride_options['drop'],
                'user_id': ride_options['user_id'],
                'ride_fare': ride_options['ride_fare'],
                'payment_type': ride_options['payment_type'],
                'car_type': car_type,
                'timestamp': datetime.utcnow()
            }

        driver_doc = driver_rides.find_one({'driver_id' : driver_id})

        if driver_doc:
            result = driver_rides.update_one(
                {'driver_id' : driver_id},
                {'$push' : {'ride_details' : ride_details}}
            )

            if result.modified_count == 1:
                return jsonify({'message': 'driver added successfully'}), 200
            else:
                return jsonify({'message': 'Failed to add driver'}), 500

        else:
            new_ride = {
                'driver_id': driver_id,
                'ride_details': [ride_details],
            }

            result = driver_rides.insert_one(new_ride)
            if result.inserted_id:
                return jsonify({'message': 'driver added successfully'}), 200
            else:
                return jsonify({'message': 'Failed to add driver'}), 500
            