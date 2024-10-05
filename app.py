from flask import Flask 
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config 

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

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