import boto3
from models.aplicacao import Aplicacao 
from models.projeto import Projeto
from models.user import User
from models.processo_seletivo import ProcessoSeletivo
import os 
import datetime
from dotenv import load_dotenv 
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

load_dotenv()

BUCKET_NAME = 'bucket-agil'


def upload_to_s3(file):
    try:
        session = boto3.Session()
        s3_client = session.client('s3')
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    except NoCredentialsError:
        raise Exception("Credentials not available")
    except PartialCredentialsError:
        raise Exception("Partial credentials")
    except ClientError as e:
        raise Exception(e)

def create_aplicacao(data: dict):
    """
        Criar uma aplicacao.
        Permissionamento: estudante 

        form data:
            {
                "estudante": "id do estudante",
                "projeto": "id do projeto",
                "processo_seletivo": "id do processo seletivo",
                "estudante_lattes": "link do lattes do aluno",
                "aplicacao_pdf": pdf da aplicacao

            }

    """
    file = data.files['aplicacao_pdf']
    projeto_id = data.form['projeto']
    estudante_id = data.form['estudante']
    processo_id = data.form['processo_seletivo']
    estudante_lattes = data.form['estudante_lattes']

    projeto = Projeto.get_by_id(projeto_id)
    if not projeto:
        return {'error': 'Projeto does not exist'}, 400

    estudante = User.get_by_id(estudante_id)
    if not estudante:
        return {'error': 'Estudante does not exist'}, 400
    if estudante['role'] != 'estudante':
        return {'error': 'User is not a student'}, 400

    processo = ProcessoSeletivo.get_by_id(processo_id)
    if not processo:
        return {'error': 'Processo Seletivo does not exist'}, 400


    pdf_url = upload_to_s3(file)

    if datetime.datetime.now() < processo.data_encerramento:
        aplicacao = Aplicacao(pdf_url=pdf_url, estudante=estudante_id, projeto=projeto_id, processo_seletivo=processo_id, estudante_lattes=estudante_lattes)

        aplicacao.save()

        projeto.aplicacoes.append(aplicacao.id)
        projeto.update(projeto.dict())

        return {"message": f"Applicacao submited"} , 201
    
    return {'error': 'Processo Seletivo has ended'}, 400

def get_aplicacao(id: str):
    aplicacao = Aplicacao.get_by_id(id)
    return aplicacao.dict()

def get_aplicacao_by_professor(id: str):
    aplicacoes = Aplicacao.get_by_professor(id)
    return [aplicacao.dict() for aplicacao in aplicacoes]

def get_aplicacao_by_projeto(id: str):
    aplicacoes = Aplicacao.get_by_professor(id)
    return [aplicacao.dict() for aplicacao in aplicacoes]

def get_all_aplicacoes():
    aplicacoes = Aplicacao.get_all()
    return [aplicacao.dict() for aplicacao in aplicacoes]

def update_aplicacao(data: dict):
    aplicacao = Aplicacao.get_by_id(data['id'])
    new_aplicacao = Aplicacao(**data).dict()
    new_aplicacao['id'] = data['id']
    aplicacao.update(new_aplicacao)

    updated_aplicacao = Aplicacao.get_by_id(data['id'])
    updated_aplicacao = updated_aplicacao.dict()
    updated_aplicacao['id'] = data['id']

    return {'message': f'Aplicação atualizada com sucesso com id {data["id"]}'}, 201

def delete_aplicacao(id: str):
    aplicacao = Aplicacao.get_by_id(id)
    aplicacao.delete()
    return {'message': f'Aplicação deletada com sucesso com id {id}'}, 200

def check_processo_date(data: dict):
    processo = ProcessoSeletivo.get_by_id(data[0]['processo_seletivo'])
    if not processo:
        return {'error': 'Processo Seletivo does not exist'}, 400

    if datetime.datetime.now() < processo.data_encerramento:
        return False

    return True
    

