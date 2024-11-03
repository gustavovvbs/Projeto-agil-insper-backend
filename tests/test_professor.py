import requests
import os
from dotenv import load_dotenv

load_dotenv('test_auth_tokens')
auth_tokens = {
    "coordinator":os.environ.get("COORDINATOR"),
    "professor": os.environ.get("PROFESSOR"),
    "student": os.environ.get("STUDENT")
    }

def test_get_professor_by_id_200():
    url = 'https://projeto-agil-insper-backend.onrender.com/professor/671f7d61241759e9bc1869e7'
    answer = requests.get(url) 
    assert answer.status_code == 200

def test_get_professor_by_id_404():
    url = 'https://projeto-agil-insper-backend.onrender.com/professor/671f7d61241759e9bc1869e6'
    answer = requests.get(url) 
    assert answer.status_code == 404

def test_get_all_professor_200():
    url = "https://projeto-agil-insper-backend.onrender.com/professor"
    answer = requests.get(url) 
    assert answer.status_code == 200

def test_get_all_professor_404():
    #se não existirem professores
    url = "https://projeto-agil-insper-backend.onrender.com/professor"
    answer = requests.get(url) 
    assert answer.status_code == 404