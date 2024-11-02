from pymongo import ReturnDocument
from datetime import timedelta, datetime
from database import init_db
from pytz import timezone
from mail import mail

br_tz = timezone("America/Sao_Paulo")

class ImportantEmailsStudent:
    @staticmethod
    def gather_all_students_emails():
        db = init_db()
        alunos = db.users.find({"role": "student"}, {"email": 1, "_id": 0})
        return [aluno.get('email') for aluno in alunos if aluno.get('email')]

    @staticmethod
    def gather_important_student_dates():
        now = datetime.now(br_tz)
        time_threshold = now + timedelta(days=5)
        db = init_db()
        important_processes = db.selection_process.find_and_modify(
            {"data": {"$lte": time_threshold}, "notified": {"$ne": True}},
            {"$set": {"notified": True}},
            projection={"nome": 1, "data": 1},
            return_document=ReturnDocument.AFTER
        )
        return important_processes if important_processes else []

    @staticmethod
    def send_email_student(important_process, emails):
        if not emails or not important_process:
            return False
            
        for process in important_process:
            try:
                mail.send_message(
                    subject="Tempos importantes estão chegando",
                    body=f"O processo {process['nome']} está chegando e acontecerá dia {process['data'].strftime('%d/%m/%Y')}",
                    recipients=emails
                )
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                continue
        return True

class ImportantEmailsProfessor:
    @staticmethod
    def gather_all_professors_emails():
        db = init_db()
        professors = db.users.find({"role": "professor"}, {"email": 1, "_id": 0})
        return [prof.get('email') for prof in professors if prof.get('email')]

    @staticmethod
    def gather_important_professor_dates():
        # Implementation pending based on professor proposal system
        return []

    @staticmethod
    def send_email_professor(important_process, emails):
        if not emails or not important_process:
            return False
            
        for process in important_process:
            try:
                mail.send_message(
                    subject="O prazo está chegando ao fim",
                    body="Implementação pendente",  # Add proper message
                    recipients=emails
                )
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                continue
        return True

def handle_important_emails():
    """Main function to handle both student and professor emails"""
    # Handle student emails
    student_object = ImportantEmailsStudent()
    important_processes = student_object.gather_important_student_dates()
    if important_processes:
        emails = student_object.gather_all_students_emails()
        if emails:
            student_object.send_email_student(important_processes, emails)

    # Handle professor emails
    professor_object = ImportantEmailsProfessor()
    important_processes = professor_object.gather_important_professor_dates()
    if important_processes:
        emails = professor_object.gather_all_professors_emails()
        if emails:
            professor_object.send_email_professor(important_processes, emails)