from flask import current_app
from run import mongo 
from run import mail
from app import scheduler
from pymongo import ReturnDocument
from datetime import timedelta, datetime
from pytz import timezone

br_tz = timezone("America/Sao_Paulo")

class ImportantEmailsStudent:

    @staticmethod
    def gather_all_students_emails():
        alunos = mongo.db.users.find({"role": {"$eq": "student"}}, {"email": 1})
        return list(alunos.values())

    @staticmethod
    def gather_important_student_dates():
        now = datetime.now(br_tz)
        time_threshold = now + timedelta(days=5)
        important_processes = list(mongo.db.selection_process._find_and_modify({"data": {"$lte": time_threshold}, "notified": {"$ne": True}}, {"$set": {"notified": True}}, projection={"nome": 1, "data": 1}, return_document=ReturnDocument.AFTER))
        return important_processes

    @staticmethod
    def send_email_student(important_process, emails):
        for process in important_process:
            mail.send_message(
                subject="Tempos importantes estão chegando",
                body=f"O processo {process["nome"]} está chegando e acontecerá dia {process["data"]}",
                recipients=emails
        )

class ImportantEmailsProfessor:
    
    @staticmethod
    def gather_all_professors_emails():
        professors = mongo.db.users.find({"role": {"$eq": "professor"}}, {"email": 1})
        return list(professors.values())
    
    @staticmethod
    def gather_important_professor_dates():
        # a gente vai ter um sistema de propostas? "Os professores recebem quando o prazo para avaliação das propostas (aprovar/reprovar) está chegando ao fim."
        return None
    
    def send_email_professor(important_process, emails):
        for process in important_process:
            mail.send_message(
                subject = "O prazo está chegando ao fim",
            )
        

@staticmethod
def handle_logic_student():
    student_object = ImportantEmailsStudent()
    important_processes = student_object.gather_important_student_dates()
    if not important_processes:
        return None
    emails = student_object.gather_all_students_emails()
    if not emails:
        return None
    student_object.send_email_student(important_processes, emails)
    return True

@staticmethod
def handle_logic_professor():
    professor_object = ImportantEmailsProfessor()
    important_processes = professor_object.gather_important_professor_dates()
    if not important_processes:
        return None
    emails = professor_object.gather_all_professors_emails()
    if not emails:
        return None
    professor_object.send_email_professor(important_processes, emails)
    return True

