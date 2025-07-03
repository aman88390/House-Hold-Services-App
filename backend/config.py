import os
from datetime import timedelta  

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app6.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    ACCESS_TOKEN_EXPIRY_MINUTES = 120  
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')  
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    EXPORT_FOLDER = "/path/to/export/folder"  
    ADMIN_EMAIL = "admin@example.com" 
    