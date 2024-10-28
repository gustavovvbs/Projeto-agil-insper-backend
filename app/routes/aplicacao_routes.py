from flask import Flask, Blueprint, request, jsonify
from database import init_db
from models.aplicacao import Aplicacao 
from models.professor import Professor 
from models.estudante import Estudante 
from models.processo_seletivo import ProcessoSeletivo 
from controllers.aplicacao_controller import create_aplicacao, get_all_aplicacoes
from utils.jwt_auth import decode_jwt_token
from utils.auth_decorator import role_required 

aplicacao_routes = Blueprint('aplicacao', __name__)

@aplicacao_routes.route('/', methods=['POST'])
@role_required(['estudante'])
def create():
    """
        Criar uma aplicacao.
        Permissionamento: estudante 

        form data:
            {
                "estudante": "id do estudante",
                "projeto": "id do projeto",
                "processo_seletivo": "id do processo seletivo",
                "estudante_lattes": "link do lattes do aluno",
                "aplicacao_pdf": pdf da aplicacao

            }

    """

    response = create_aplicacao(request)

    return response

@aplicacao_routes.route('/' , methods=['GET'])
@role_required(['coordenador'])
def get_all():
    """
        Retorna todas as aplicacoes.
    """
    aplicacoes = get_all_aplicacoes()
    return jsonify(aplicacoes)

