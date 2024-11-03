from controllers.professor_controller import get_by_id, get_all
from flask import Blueprint

professor_routes = Blueprint('professor', __name__)

@professor_routes.route('/<id>', methods=['GET'])
def get_professor_by_id(id):
    response = get_by_id(id)

    return response

@professor_routes.route('/', methods=['GET'])
def get_all_professores():
    response = get_all()

    return response
