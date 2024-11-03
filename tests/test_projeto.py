import requests
from dotenv import load_dotenv
import os
load_dotenv('auth_tokens')
auth_token = {
    'professor': os.environ.get("")
}

def test_create_projeto_201():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMwMjc3LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.3OS3dZ4vfXatcpdrY1fqtIBY3vNk95UNgQcnZevdWRg"}
    data = {"processo_seletivo":"671f811a2e33a765fc56eb7a","professor": "671f7d61241759e9bc1869e7","temas": ["engenharia"],"descricao": "projeto de engenharia","titulo": "teste titulo 2"}
    url = "https://projeto-agil-insper-backend.onrender.com/projeto"
    answer = requests.post(url=url, headers=headers, json=data)
    assert answer.status_code == 201

def test_create_projeto_400():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMwMjc3LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.3OS3dZ4vfXatcpdrY1fqtIBY3vNk95UNgQcnZevdWRg"}
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

#falta o edit