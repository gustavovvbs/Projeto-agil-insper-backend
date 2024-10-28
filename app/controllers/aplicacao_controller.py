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
    file = data.files['application_pdf']
    pdf_url = upload_to_s3(file)
    projeto_id = data.form['projeto_id']
    estudante_id = data.form['estudante_id']
    processo_id = data.form['processo_id']
    estudante_lattes = data.form['estudante_lattes']

    aplicacao = Aplicacao(pdf_url=pdf_url, estudante=estudante_id, projeto=projeto_id, processo_seletivo=processo_id, estudante_lattes=estudante_lattes)

    aplicacao.save()

    return {"message": f"Aplicação criada com sucesso com id{aplicacao.id} "} , 201
