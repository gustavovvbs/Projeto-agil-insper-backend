from vectorstore import initialize_vector_store
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI 
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from typing import List, Optional, Dict
import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from openai import OpenAI 

client = OpenAI()
load_dotenv()

VECTOR_STORE = initialize_vector_store()
RETRIEVER = VECTOR_STORE.as_retriever()

class Professor(BaseModel):
    name:str 
    llm_response: str
    photo: str
    email: str
    research_area: str 
    description: str

def respond_query(
    theme_enjoyed: str, 
    course: str, 
    academic_or_product: str,
    semester: str,
    has_idea: str,
    idea: Optional[str],
):
    llm = ChatOpenAI(model = 'gpt-4o-mini')

    system_prompt = """
    Você vai receber as respostas a um formulário de um aluno que expressa seus interesses em pesquisa. A partir das informações fornecidas, sua tarefa é identificar a área de interesse do aluno e, se ele tiver uma ideia de projeto, traduzi-la em uma descrição de temas de pesquisa.

    Aqui estão os parâmetros que você deve considerar:
    - `theme_enjoyed`: A área de interesse que o aluno aprecia.
    - `course`: O curso em que o aluno está matriculado.
    - `academic_or_product`: Indica se o aluno está mais interessado em pesquisa acadêmica ou em desenvolvimento de produtos.
    - `semester`: O semestre atual do aluno.
    - `has_idea`: Um valor booleano que indica se o aluno tem uma ideia de projeto (sim ou não).
    - `idea`: Se `has_idea` for "sim", forneça a ideia do projeto. Se for "não", deixe este campo vazio.

    Se o aluno tiver uma ideia de projeto, crie uma descrição que inclua:
    1. A área de interesse (de `theme_enjoyed`).
    2. A natureza do curso (de `course`).
    3. O tipo de pesquisa (de `academic_or_product`).
    4. Uma breve descrição da ideia (de `idea`).

    Caso o aluno não tenha uma ideia de projeto, forneça uma descrição da área de interesse e o curso, mas não inclua detalhes sobre uma ideia de projeto. Forneça tambem as areas de pesquisa potenciais com base nas informações fornecidas, como por exemplo, financas e desenvolvimento web.

    **Exemplo de uso**:
    1. Se `has_idea` for "sim" e `idea` for "Desenvolver um aplicativo de finanças pessoais":
    - Resposta: "O aluno tem interesse na área de finanças, está matriculado no curso de Administração, e deseja desenvolver um aplicativo de finanças pessoais como um projeto de pesquisa. Os temas de pesquisa incluem finanças corporativas e tecnologia financeira."

    2. Se `has_idea` for "não":
    - Resposta: "O aluno tem interesse na área de finanças e está matriculado no curso de Administração, mas não tem uma ideia de projeto definida no momento. Os temas de pesquisa potenciais incluem finanças corporativas e comportamento do consumidor."

    Use este modelo para construir a descrição do perfil de pesquisa do aluno com base nas respostas que você receber.
    """

    prompt_student = """ 
    Aqui está a resposta ao formulário do aluno:
        Tema de interesse: {theme_enjoyed}
        Curso: {course}
        Interesse acadêmico ou em produtos: {academic_or_product}
        Semestre: {semester}
        Tem uma ideia de projeto: {has_idea}
        Ideia de projeto: {idea}
        """

    prompt = ChatPromptTemplate.from_messages(
        [('system', system_prompt),
        ('user', prompt_student)]
    )

    chain = (
        {
            'theme_enjoyed': itemgetter('theme_enjoyed'),
            'course': itemgetter('course'),
            'academic_or_product': itemgetter('academic_or_product'),
            'semester': itemgetter('semester'),
            'has_idea': itemgetter('has_idea'),
            'idea': itemgetter('idea')
        }
        | prompt 
        |llm 
        | StrOutputParser()
    )

    student_awnser = chain.invoke({'theme_enjoyed': theme_enjoyed, 'course': course, 'academic_or_product': academic_or_product, 'semester': semester, 'has_idea': has_idea, 'idea': idea})

    
    match_promt = """ 
    Você vai receber um perfil de pesquisa de um professor e as informações extraídas do aluno. Sua tarefa é justificar por que o professor é uma boa combinação para orientar o aluno com base nas informações fornecidas.
    A reposta final será entregue ao aluno, então não se refira ao aluno na terceira pessoa, e sim utilizando "você" e "seu/sua".

    Caso algum campo esteja faltando, não mencione que existe um campo faltando, apenas forneça a resposta com base nas informações disponíveis.
    """ 

    professor_description = """
    Aqui está o perfil de pesquisa do professor: {description} e os interesses extraídos do aluno: {student_awnser}
    """

    matching_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', match_promt),
            ('user', professor_description)
        ]
    )


    queried_professors = RETRIEVER.invoke(student_awnser)
    professors_output = []
    
    chain_matching = ( 
        {
            "description": itemgetter('description'),
            "student_awnser": itemgetter('student_awnser')
        }
        |matching_prompt
        | llm
        | StrOutputParser()
    )

    for professor in queried_professors:
        reasoning = chain_matching.invoke({'description': professor.metadata['description'], 'student_awnser': student_awnser})
        professor.metadata['reasoning'] = reasoning
        professors_output.append(professor)

    return professors_output



    