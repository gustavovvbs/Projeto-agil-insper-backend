import requests
import os
from dotenv import load_dotenv

load_dotenv('test_auth_tokens')
auth_tokens = {
    "coordinator":os.environ.get("COORDINATOR"),
    "professor": os.environ.get("PROFESSOR"),
    "student": os.environ.get("STUDENT")
    }

def test_create_projeto_201():
    headers = {"Authorization": auth_tokens['coordinator']}
    data = {"processo_seletivo":"671f811a2e33a765fc56eb7a","professor": "671f7d61241759e9bc1869e7","temas": ["engenharia"],"descricao": "projeto de engenharia","titulo": "teste titulo 2"}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto"
    answer = requests.post(url=url, headers=headers, json=data)
    assert answer.status_code == 201

def test_create_projeto_400():
    headers = {"Authorization": auth_tokens['coordinator']}
    data = {}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto"
    answer = requests.post(url=url, headers=headers, json=data)
    assert answer.status_code == 400

def test_get_all_projetos_200():
    url = 'https://projeto-agil-insper-backend.onrender.com/projeto'
    answer = requests.get(url)
    assert answer.status_code == 200

def test_get_all_projetos_404():
    #se não existirem projetos
    url = 'https://projeto-agil-insper-backend.onrender.com/projeto'
    answer = requests.get(url)
    assert answer.status_code == 404

def test_get_projeto_by_id_200():
    url="https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79453"
    answer = requests.get(url)
    assert answer.status_code == 200

def test_get_projeto_by_id_404():
    url="https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79432"
    answer = requests.get(url)
    assert answer.status_code == 404

def test_edit_projeto_200():
    headers = {"Authorization": auth_tokens['professor']}
    data = {"titulo": "teste de integracao 12312"}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79453"
    answer = requests.put(url=url, headers=headers, json=data)
    assert answer.status_code == 200

def test_edit_projeto_200():
    headers = {"Authorization": auth_tokens['professor']}
    data = {}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79453"
    answer = requests.put(url=url, headers=headers, json=data)
    assert answer.status_code == 400

def test_edit_projeto_403():
    headers = {"Authorization": ""}
    data = {"titulo": "teste de integracao 12312"}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79453"
    answer = requests.put(url=url, headers=headers, json=data)
    assert answer.status_code == 403

def test_edit_projeto_404():
    headers = {"Authorization": auth_tokens['professor']}
    data = {"titulo": "teste de integracao 12312"}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto/671f927c94f45441faa79452"
    answer = requests.put(url=url, headers=headers, json=data)
    assert answer.status_code == 404