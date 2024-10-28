from flask import Flask, Blueprint, request, jsonify
from database import init_db
from models.aplicacao import Aplicacao 
from models.professor import Professor 
from models.estudante import Estudante 
from models.processo_seletivo import ProcessoSeletivo 
from controllers.aplicacao_controller import create_aplicacao
from utils.auth_decorator import role_required 

aplicacao_routes = Blueprint('aplicacao', __name__)

@aplicacao_routes.route('/', methods=['POST'])
@role_required(['estudante'])
def create():
    """
        Criar uma aplicacao.
        Permissionamento: estudante 

        Request Body:
            {
                "id_estudante": "id do estudante",
                "id_processo": "id do processo seletivo",
                "id_professor": "id do professor",
                "l
            }

    """
    data = request.get_json()
    response = create_aplicacao(data)

    return response