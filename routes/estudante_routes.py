from flask import Blueprint
from controllers.estudante_controller import get_by_id

estudante_routes = Blueprint('estudante', __name__)

@estudante_routes.route('/<id>', methods=['GET'])
def get_estudante_by_id(id):
    response = get_by_id(id)

    return response