import requests

#auth professor
def test_auth_login_professor_200():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"professor1@insper.com.br","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 200

def test_auth_login_professor_404():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"usuarioinexistente@email.com","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 404

def test_auth_login_professor_400():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"professor1@insper.com.br","password": "senhaincorreta123"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code in (400,401)

def test_auth_register_professor_201():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/register'
    data_professor = {
        "nome": "Professor2",
        "email": "professor2@insper.com.br",
        "curso": '',
        "Semestre": '',
        "role": "professor",
        "password": '',
        "area_pesquisa": 'teste',
        "descricao": 'teste'
    }
    answer = requests.post(url, headers=headers, json=data_professor)
    assert answer.status_code in (200,201)

#auth student
def test_auth_login_student_200():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"gustavovvbs@al.insper.edu.br","password":"teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 200

def test_auth_login_student_404():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"usuarioinexistente@email.com","password":"teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 404

def test_auth_login_student_400():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"gustavovvbs@al.insper.edu.br","password":"senhaincorreta123"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code in (400,401)

def test_auth_register_student_201():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/register'
    data_estudante = {
    "nome": "Gustavo",
    "email": "gustavoss8@al.insper.edu.br",
    "curso": "Ciência da Computação",
    "Semestre": "segundo",
    'role': "estudante",
    "password": None,
    "area_pesquisa": None,
    "descricao": None
    }
    answer = requests.post(url, headers=headers, json=data_estudante)
    assert answer.status_code in (200,201)
    

#auth coordination
def test_auth_login_coordinator_200():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"coordenador1@insper.com","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 200

def test_auth_login_coordinator_404():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"usuarioinexistente@email.com","password": "teste"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code == 404

def test_auth_login_coordinator_400():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/login'
    data = {"email":"coordenador1@insper.com","password": "senhaincorreta123"}
    answer = requests.post(url,headers=headers,json=data)

    assert answer.status_code in (400,401)
    
def test_auth_register_coordinator_201():
    headers = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/auth/register'
    
    data_coordenador = {
        "nome": "Coordenador2",
        "email": "coordenador2@insper.com.br",
        "curso": None,
        "Semestre": None,
        'role': "coordenador",
        "password": None,
        "area_pesquisa": None,
        "descricao": None
    }
    answer = requests.post(url, headers=headers, json=data_coordenador)

    assert answer.status_code in (200,201)

