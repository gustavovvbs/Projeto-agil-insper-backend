from flask import Flask
from database import init_db 
from routes.auth_routes import auth_routes
from routes.matchmaking_routes import matchmaking_routes
from routes.processo_routes import processo_routes
from routes.aplicacao_routes import aplicacao_routes
from routes.projeto_routes import projeto_routes
from routes.professor_routes import professor_routes
from routes.estudante_routes import estudante_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)

    db = init_db()

    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(matchmaking_routes, url_prefix='/matchmaking')
    app.register_blueprint(processo_routes, url_prefix='/processo')
    app.register_blueprint(aplicacao_routes, url_prefix = '/aplicacao')
    app.register_blueprint(projeto_routes, url_prefix = '/projeto')
    app.register_blueprint(professor_routes, url_prefix = '/professor')
    app.register_blueprint(estudante_routes, url_prefix = '/estudante')
    
    return app

app = create_app()

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)