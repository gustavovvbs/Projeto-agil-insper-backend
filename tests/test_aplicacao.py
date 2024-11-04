import requests
import os
from dotenv import load_dotenv

load_dotenv('test_auth_tokens')
auth_tokens = {
    "coordinator":os.environ.get("COORDINATOR"),
    "professor": os.environ.get("PROFESSOR"),
    "student": os.environ.get("STUDENT")
    }

def test_get_all_aplicacoes_200():
    headers = {"Authorization": auth_tokens["coordinator"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 200

def test_get_all_aplicacoes_404():
    #se não existirem aplicações
    headers = {"Authorization": auth_tokens["coordinator"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 404

def test_get_aplicacoes_por_professor_200():
    headers = {"Authorization": auth_tokens["professor"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/professor"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 200

def test_get_aplicacoes_por_professor_401():
    headers = {"Authorization": ""}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/professor"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 401

def test_get_aplicacoes_por_professor_404():
    #se não existirem aplicações por professor
    headers = {"Authorization": auth_tokens["professor"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/professor"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 404

def test_get_aplicacoes_por_projeto_200():
    headers = {"Authorization": auth_tokens["professor"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/projeto/671f912ed6c196d2c1020978"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 200

def test_get_aplicacoes_por_projeto_401():
    headers = {"Authorization": ''}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/projeto/671f912ed6c196d2c1020978"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 401

def test_get_aplicacoes_por_projeto_404():
    headers = {"Authorization": auth_tokens["professor"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/projeto/671f912ed6c196d2c1020978"
    answer = requests.get(url, headers=headers)
    assert answer.status_code == 404

def test_aprova_aplicacao_200():
    headers = {"Authorization": auth_tokens["professor"]}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/671fc21a6c57e09acfb4b84b/projeto/671f927c94f45441faa79453"
    answer = requests.put(url=url, headers=headers)
    assert answer.status_code == 200

def test_aprova_aplicacao_400():
    headers = {"Authorization": auth_tokens['professor']}
    url1 = "https://projeto-agil-insper-backend.onrender.com/aplicacao/672fc21a6c57e09acfb4b84b/projeto/671f927c94f45441faa79453"
    answer1 = requests.put(url=url1, headers=headers)
    url2 = "https://projeto-agil-insper-backend.onrender.com/aplicacao/671fc21a6c57e09acfb4b84b/projeto/6712927c94f45441faa79453"
    answer2 = requests.put(url=url2, headers=headers)
    assert answer1.status_code == 400 and answer2.status_code == 400

def test_aprova_aplicacao_403():
    headers = {"Authorization": ''}
    url = "https://projeto-agil-insper-backend.onrender.com/aplicacao/671fc21a6c57e09acfb4b84b/projeto/671f927c94f45441faa79453"
    answer = requests.put(url=url, headers=headers)
    assert answer.status_code == 403

#falta o create aplicação