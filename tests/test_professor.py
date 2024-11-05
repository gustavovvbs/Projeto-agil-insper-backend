import requests

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
    assert not(answer.status_code == 404)