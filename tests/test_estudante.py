import requests
import os
from dotenv import load_dotenv

load_dotenv('test_auth_tokens')
auth_tokens = {
    "coordinator":os.environ.get("COORDINATOR"),
    "professor": os.environ.get("PROFESSOR"),
    "student": os.environ.get("STUDENT")
    }

def test_get_by_id_student_200():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/estudante/671e4d596b068eb5df511914'
    answer = requests.get(headers=headers, url=url)
    
    assert answer.status_code == 200

def test_get_by_id_student_404():
    # o id: 671e4d596b068eb5df511914 é inválido
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/estudante/671e4d596b068eb5df511913'
    answer = requests.get(headers=headers, url=url)

    assert answer.status_code == 404