import requests

def test_create_processo_201():
    headers = {'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMwMjc3LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.3OS3dZ4vfXatcpdrY1fqtIBY3vNk95UNgQcnZevdWRg"}
    data = {"data_encerramento": "2024-11-02","titulo": "processo 4"}
    url = 'https://projeto-agil-insper-backend.onrender.com/processo'
    answer = requests.post(url, headers=headers, json=data)
    assert answer.status_code == 201

def test_create_processo_400():
    headers = {'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMwMjc3LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.3OS3dZ4vfXatcpdrY1fqtIBY3vNk95UNgQcnZevdWRg"}
    data = {}
    url = 'https://projeto-agil-insper-backend.onrender.com/processo'
    answer = requests.post(url, headers=headers, json=data)
    assert answer.status_code == 400

def test_get_processo_id_200():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7a'
    answer = requests.get(url)
    assert answer.status_code == 200

def test_get_processo_id_400():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7b'
    answer = requests.get(url)
    assert answer.status_code == 404

def test_get_all_processos_200():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo'
    answer = requests.get(url)
    assert answer.status_code == 200

def test_get_all_processos_404():
    #se não existir nenhum processo
    url = 'https://projeto-agil-insper-backend.onrender.com/processo'
    answer = requests.get(url)
    assert answer.status_code == 404

def test_edit_processos_201():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7a'
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMxMjY0LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.aaelUwtyl-0X7KahZGO_ZsaLlYZXdRLFE91gzzgCbUY'}
    data = {"data_encerramento": "2024-10-22"}
    answer = requests.put(url, headers=headers, json=data)
    if answer.status_code == 400:
        data = {"data_encerramento": "2024-10-23"}
        answer = requests.put(url, headers=headers, json=data)
    assert answer.status_code == 201

def test_edit_processos_403():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7a'
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2vyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMxMjY0LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.aaelUwtyl-0X7KahZGO_ZsaLlYZXdRLFE91gzzgCbUY'}
    data = {"data_encerramento": "2024-10-22"}
    answer = requests.put(url, headers=headers, json=data)
    assert answer.status_code == 403

def test_edit_processos_400():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7a'
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMxMjY0LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.aaelUwtyl-0X7KahZGO_ZsaLlYZXdRLFE91gzzgCbUY'}
    data = {}
    answer = requests.put(url, headers=headers, json=data)
    assert answer.status_code == 400

def test_edit_processos_404():
    url = 'https://projeto-agil-insper-backend.onrender.com/processo/671f811a2e33a765fc56eb7b'
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjcxZTkyYTUzY2EzZjEzOWRiODgxYjk2IiwiZXhwIjoxNzMwNzMxMjY0LCJyb2xlIjoiY29vcmRlbmFkb3IifQ.aaelUwtyl-0X7KahZGO_ZsaLlYZXdRLFE91gzzgCbUY'}
    data = {"data_encerramento": "2024-10-22"}
    answer = requests.put(url, headers=headers, json=data)
    assert answer.status_code == 404

#falta o delete


