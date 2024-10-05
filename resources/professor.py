from flask import Blueprint, request, jsonify
from app import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson.objectid import ObjectId
from datetime import datetime
from utils.helpers import is_professor

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    claims = get_jwt()
    if not is_professor(claims):
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    required_fields = ['title', 'description', 'requirements', 'selection_process_id', 'application_deadline']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing fields."}), 400

    data['created_by'] = ObjectId(get_jwt_identity())
    data['selection_process_id'] = ObjectId(data['selection_process_id'])
    data['application_deadline'] = datetime.strptime(data['application_deadline'], '%Y-%m-%d')
    data['status'] = 'open'

    result = mongo.db.projects.insert_one(data)
    return jsonify({"message": "Project sent.", "id": str(result.inserted_id)}), 201

# mandar os projetos, e aprovar/reprovar proposta dos aluno
