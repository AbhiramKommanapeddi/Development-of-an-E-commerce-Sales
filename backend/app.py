from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

# Import db from models
from models import db

# Initialize other Flask extensions
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce_chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page.'
    
    # Import models (import after db initialization)
    from models import User, Product, ChatMessage, Category
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables and populate with sample data
    with app.app_context():
        db.create_all()
        
        # Check if database is empty and populate with sample data
        if Product.query.count() == 0:
            from utils.database import populate_database
            populate_database()
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"🔍 DEBUG: Token expired for user {jwt_payload['sub']}")
        return {'msg': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"🔍 DEBUG: Invalid token: {error}")
        return {'msg': 'Invalid token'}, 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"🔍 DEBUG: Missing token: {error}")
        return {'msg': 'Authorization token is required'}, 401
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
