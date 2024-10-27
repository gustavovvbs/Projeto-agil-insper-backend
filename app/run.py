from flask import Flask 
from database import init_db 
from routes.auth_routes import auth_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db = init_db()

    app.register_blueprint(auth_routes, url_prefix='/auth')

    return app

app = create_app()

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)