from flask import Flask 
from database import init_db 
from routes.auth_routes import auth_routes
from routes.matchmaking_routes import matchmaking_routes
from routes.processo_routes import processo_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db = init_db()

    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(matchmaking_routes, url_prefix='/matchmaking')
    app.register_blueprint(processo_routes, url_prefix='/processo')
    
    return app

app = create_app()

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)