from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    return datetime.now(IST)

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String , nullable=False)
    username = db.Column(db.String(54), unique=True, nullable=False)
    email = db.Column(db.String(432), unique=True, nullable=False)
    password = db.Column(db.String(564), nullable=False)
    role = db.Column(db.Enum('admin', 'professional', 'customer'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    block = db.Column(db.Boolean, default=False)

    professional = db.relationship('ServiceProfessional', back_populates='user', uselist= False)  
    customer = db.relationship('Customer', back_populates='user')
    requests = db.relationship('ServiceRequest', back_populates = 'user') 

class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(700), nullable=True)
    
    services = db.relationship('Service', back_populates='service_type')  

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(67), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=False)
    
    service_type = db.relationship('ServiceType', back_populates='services') 
    requests = db.relationship('ServiceRequest', back_populates='service')  
    serviceprofessionals = db.relationship('ServiceProfessional', back_populates='service', uselist=False)  


class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=True,)
    address = db.Column(db.String(500), nullable=True)
    pin_code = db.Column(db.String(18), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', back_populates='professional')  
    requests = db.relationship('ServiceRequest', back_populates='professional')  
    service = db.relationship('Service', back_populates='serviceprofessionals')  


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    pin_code = db.Column(db.String(18), nullable=False)
    verified = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='customer') 
    # requests = db.relationship('ServiceRequest', back_populates='customer')  

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=False)
    date_of_request = db.Column(db.DateTime, default=get_ist_now)
    date_of_completion = db.Column(db.DateTime, nullable=True, default=None)
    service_status = db.Column(db.Enum('requested', 'assigned', 'closed','rejected'), default='requested')
    date_time_of_service = db.Column(db.DateTime, default=get_ist_now)
    rating = db.Column(db.Integer, nullable= True)  
    review = db.Column(db.String(300), nullable=True)
  
    service = db.relationship('Service', back_populates='requests') 
    user = db.relationship('User', back_populates='requests')  
    professional = db.relationship('ServiceProfessional', back_populates='requests')  



