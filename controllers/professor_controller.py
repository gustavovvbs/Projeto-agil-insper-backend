from models.professor import Professor 
from models.projeto import Projeto
from models.aplicacao import Aplicacao
def get_by_id(id: str):
    professor = Professor.get_by_id(id)
    if not professor:
        return {"message": "Professor not found"}, 404

    return professor.dict(), 200

def get_all():
    professores = Professor.get_all()
    if not professores:
        return {"message": "No professors found"}, 404
    professores = [professor.dict() for professor in professores]
    return professores, 200

def get_projects_by_professor(id):
    projects = Projeto.get_all_by_professors(id)
    if not projects:
        return {"message": "No projects found"}, 404
    projects = [project.dict() for project in projects]
    return projects, 200

def get_project_by_id(id):
    project = Projeto.get_by_id(id)
    if not project:
        return {"message": "No project found"}, 404
    return project, 200

def get_aplicacao_by_projeto(id: str):
    aplicacoes = Aplicacao.get_by_projeto(id)
    return [aplicacao.dict() for aplicacao in aplicacoes]

def get_applications_by_project_id(id):
    project = Projeto.get_by_id(id)
    if not project:
        return {"message": "No project found"}, 404
    applications = get_aplicacao_by_projeto(id)
    if not applications:
        return {"message": "No applications found for this project"}, 200
    applications = [application.dict() for application in applications]
    return applications, 200

def get_aplicacao(id: str):
    aplicacao = Aplicacao.get_by_id(id)
    return aplicacao.dict()