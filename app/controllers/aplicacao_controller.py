import boto3
from models.aplicacao import Aplicacao 
import os 
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
    file = data.files['aplicacao_pdf']
    pdf_url = upload_to_s3(file)
    projeto_id = data.form['projeto']
    estudante_id = data.form['estudante']
    processo_id = data.form['processo_seletivo']
    estudante_lattes = data.form['estudante_lattes']

    aplicacao = Aplicacao(pdf_url=pdf_url, estudante=estudante_id, projeto=projeto_id, processo_seletivo=processo_id, estudante_lattes=estudante_lattes)

    aplicacao.save()

    return {"message": f"Aplicação criada com sucesso com id{aplicacao.id} "} , 201

def get_aplicacao(id: str):
    aplicacao = Aplicacao.get_by_id(id)
    return aplicacao.dict()

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
