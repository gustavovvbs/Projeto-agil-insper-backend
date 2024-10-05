from flask import Blueprint, request, jsonify
from app import mongo 
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson.objectid import ObjectId
from datetime import datetime 
from utils.helpers import is_coordination

coordination_bp = Blueprint('coordination', __name__)

@coordination_bp.route('/selection_process', methods=['POST'])
@jwt_required()
def create_selection_process():
    claims = get_jwt()
    if not is_coordination(claims):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    required_fields = ['modality', 'title', 'description', 'course', 'period', 'end_date']

    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields'}), 400

    data['created_by'] = ObjectId(get_jwt_identity())
    data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
    data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')

    result = mongo.db.selection_processes.insert_one(data)
    return jsonify({'Selection process created': str(result.inserted_id)}), 201

#fzer o crud dos processo seletivo aq