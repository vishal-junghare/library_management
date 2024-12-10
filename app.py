from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from resources.auth import auth_bp
from resources.librarian import librarian_bp
from resources.user import user_bp

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(librarian_bp, url_prefix="/librarian")
app.register_blueprint(user_bp, url_prefix="/user")

# Create database tables
@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
