from flask import Blueprint, request, jsonify
from app import mongo
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects/open', methods=['GET'])
@jwt_required()
def get_open_projects():
    projects = mongo.db.projects.find({"status": "open"})
    projects_list = []
    for project in projects:
        project['_id'] = str(project['_id'])
        project['created_by'] = str(project['created_by'])
        project['selection_process_id'] = str(project['selection_process_id'])
        projects_list.append(project)
    return jsonify(projects_list), 200

# cada projeto eh linkado a uma aplicacao, q cada aplicacao eh linkada a um processo seletivo