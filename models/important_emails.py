from flask import current_app
from app import mongo 
from app import mail
from app import scheduler
from pymongo import ReturnDocument
from flask_mail import Message
from bson import ObjectId
import datetime
import pytz

br_tz = pytz.timezone("America/Sao_Paulo")


@staticmethod
def gather_all_students_emails():
    return list(mongo.db.users.find({}, {"email": 1}).values())

@staticmethod
def gather_important_student_dates():
    now = datetime.datetime.now(br_tz)
    time_threshold = now + datetime.timedelta(days=5)
    important_processes = list(mongo.db.selection_process._find_and_modify({"data": {"$lte": time_threshold}, "notified": {"$ne": True}}, {"$set": {"notified": True}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER))
    return important_processes

@staticmethod
def create_email_student(important_process, emails):
    for process in important_process:
        mail.send_message(
            subject="Tempos importantes estão chegando",
            body=f"O processo {process["nome"]} está chegando e acontecerá dia {process["data"]}",
            recipients=emails
        )

@staticmethod
def handle_logic_student():
    important_processes = gather_important_student_dates()
    if not important_processes:
        return None
    emails = gather_all_students_emails()
    if not emails:
        return None
    create_email_student(important_processes, emails)
    return True
scheduler.add_job(handle_logic_student, "interval", days=1)