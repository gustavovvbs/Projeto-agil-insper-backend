import pytest
import requests

#auth professor
def test_auth_professor():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"professor1@insper.com.br","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 200


#auth student
def test_auth_student():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"gustavovvbs@al.insper.edu.br","password":"teste"}
    answer = requests.post(url,headers=headers,json=data)

    if answer.status_code == 200:
        assert True
    else:
        assert False

#auth coordination
def test_auth_coordinator():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"coordenador1@insper.com","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    if answer.status_code == 200:
        assert True
    else:
        assert False


