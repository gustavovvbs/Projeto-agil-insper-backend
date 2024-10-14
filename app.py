from flask import Flask 
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config 

mongo = PyMongo()
jwt = JWTManager()
mail = Mail()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)
   

    app.config["EMAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "your_mail@gmail.com"
    app.config["MAIL_PASSWORD"] = "your_email_password"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail.init_app(app)
    from resources.auth import auth_bp 
    from resources.coordination import coordination_bp
    from resources.professor import professor_bp
    from resources.student import student_bp
    from resources.project import project_bp
    from resources.application import application_bp 
    from resources.message import message_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(coordination_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(message_bp)

    return app 