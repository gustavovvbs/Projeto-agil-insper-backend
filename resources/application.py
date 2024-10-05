from flask import Blueprint, request, jsonify, current_app
from app import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from utils.helpers import is_student, allowed_file

application_bp = Blueprint('application', __name__)

@application_bp.route('/applications', methods=['POST'])
@jwt_required()
def submit_application():
    claims = get_jwt()
    if not is_student(claims):
        return jsonify({"message": "Unauthorized."}), 403

    if 'pdf_proposal' not in request.files:
        return jsonify({"message": "Please, send a pdf file."}), 400

    file = request.files['pdf_proposal']
    if file.filename == '':
        return jsonify({"message": "No file was selected."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        return jsonify({"message": "We dont suppor this file extension, send a pdf file."}), 400

    data = request.form.to_dict()
    required_fields = ['project_id']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields."}), 400

    application = {
        "project_id": ObjectId(data['project_id']),
        "student_id": ObjectId(get_jwt_identity()),
        "pdf_proposal": filepath,
        "form_data": data,
        "status": "submitted",
        "created_at": datetime.utcnow(),
    }

    result = mongo.db.applications.insert_one(application)
    return jsonify({"message": "Application sent.", "id": str(result.inserted_id)}), 201