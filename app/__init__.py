from flask import Flask
from config import config
from flask_login import LoginManager
from .controllers.userController import getUserById
from .models.user import User

def create_app(config_name='development'):
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])

    login_manager_app.init_app(app)
    
    from app.routes import home_bp,property_bp,auth_bp

    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(property_bp)
    app.register_blueprint(auth_bp)
    
    return app

login_manager_app = LoginManager()
login_manager_app.login_view = 'auth.login'


@login_manager_app.user_loader
def load_user(id):
    user_data = getUserById(id)  # Esta función debe devolver un diccionario
    if user_data:
        return User(
            id=user_data['id'],
            email=user_data['email'],
            password=user_data['password'],
            name=user_data['name']
        )
    return None