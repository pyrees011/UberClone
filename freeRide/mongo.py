from flask import Blueprint, request, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import random

mongo = Blueprint('mongo', __name__)

uri = "mongodb+srv://RaunakBhansali:951203@cluster0.reeyyqp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['acoount']
ride_request = db['ride_request']

@mongo.route('/add_request', methods=['POST', 'GET'])
@login_required
def add_request():
    if request.method == "POST":
        data = request.json
        request_id = random.randint(1000,9999)
        car_type = data.get('car_type')
        ride_details = {
            'request_id': request_id,
            'pickup': data.get('pickup'),
            'drop': data.get('drop'),
            'pickup_time': data.get('pickup_time'),
            'ride_fare': data.get('ride_fare'),
            'user_id' : current_user.id,
            'payment_type': data.get('payment_type'),
            'status' : 'requested',
            'timestamp': datetime.utcnow()
        }

        request_doc = ride_request.find_one({'car_type' : car_type})

        if request_doc:
            result = ride_request.update_one(
                {'car_type' : car_type},
                {'$push' : {'ride_details' : ride_details}}
            )

            if result.modified_count == 1:
                return jsonify({'request_id' : request_id, 'car_type': car_type}), 200
            else:
                return jsonify({ 'message' : 'task not found'}), 404

        else:
            new_ride = {
                'car_type': car_type,
                'ride_details': [ride_details],
            }

            result = ride_request.insert_one(new_ride)

            if result.inserted_id:
                return jsonify({'request_id' : request_id, 'car_type': car_type}), 200
            else:
                return jsonify({ 'message' : 'task not found'}), 404
    

@mongo.route('/update_request', methods=['POST', 'GET'])
def update_request():
    data = request.json
    status_change = data.get('status')
    car_type = data.get('car_type')
    request_id = int(data.get('request_id'))

    result = ride_request.update_one(
        {'car_type': car_type, 'ride_details.request_id': request_id},
        {'$set': {
            'ride_details.$.status': status_change  # Use '$' here to update the correct item
        }})
    
    current_app.logger.info(f"Modified count: {result.modified_count}")

    if result.modified_count == 1:
        # return redirect(url_for('blogs.getblogs'))
        return jsonify({'message' : 'task updated successfully'}), 200
    else:
        return jsonify({ 'message' : 'task not found'}), 404