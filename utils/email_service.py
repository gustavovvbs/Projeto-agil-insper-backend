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
        try:
            # Changed to find() instead of find_one_and_update() to get multiple processes
            important_processes = list(db.selection_process.find(
                {
                    "data": {"$lte": time_threshold},
                    "notified": {"$ne": True}
                },
                {"nome": 1, "data": 1, "_id": 1}
            ))
            
            # Update the notified status for all found processes
            if important_processes:
                process_ids = [proc["_id"] for proc in important_processes]
                db.selection_process.update_many(
                    {"_id": {"$in": process_ids}},
                    {"$set": {"notified": True}}
                )
            
            return important_processes
        except Exception as e:
            print(f"Error gathering student dates: {str(e)}")
            return None

    @staticmethod
    def send_email_student(important_processes, emails):
        if not emails or not important_processes:
            return False
        
        try:
            # Send one email with all upcoming processes
            process_list = "\n".join([
                f"- {process['nome']}: {process['data'].strftime('%d/%m/%Y')}"
                for process in important_processes
            ])
            
            mail.send_message(
                subject="Processos importantes estão chegando",
                body=f"Os seguintes processos estão chegando:\n\n{process_list}",
                recipients=emails
            )
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

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
    def send_email_professor(important_processes, emails):
        if not emails or not important_processes:
            return False
        
        try:
            process_list = "\n".join([
                f"- Process: {process.get('name', 'Unknown')}"
                for process in important_processes
            ])
            
            mail.send_message(
                subject="O prazo está chegando ao fim",
                body=f"Os seguintes processos precisam de sua atenção:\n\n{process_list}",
                recipients=emails
            )
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

def handle_important_emails():
    """Main function to handle both student and professor emails"""
    success = True
    
    # Handle student emails
    try:
        student_object = ImportantEmailsStudent()
        important_processes = student_object.gather_important_student_dates()
        if important_processes:
            emails = student_object.gather_all_students_emails()
            if emails:
                if not student_object.send_email_student(important_processes, emails):
                    success = False
    except Exception as e:
        print(f"Error handling student emails: {str(e)}")
        success = False

    # Handle professor emails
    try:
        professor_object = ImportantEmailsProfessor()
        important_processes = professor_object.gather_important_professor_dates()
        if important_processes:
            emails = professor_object.gather_all_professors_emails()
            if emails:
                if not professor_object.send_email_professor(important_processes, emails):
                    success = False
    except Exception as e:
        print(f"Error handling professor emails: {str(e)}")
        success = False

    return success
