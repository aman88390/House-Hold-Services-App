from flask import Blueprint, request, jsonify,session,Flask, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from application.model import db, User, ServiceType, Service, ServiceProfessional, Customer, ServiceRequest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_, func
from extensions import cache
from application.tasks import export_service_requests_task
import os
import io 
from celery.result import AsyncResult
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import get_jwt_identity
import matplotlib.pyplot as plt



app = Blueprint('app', __name__)

def create_jwt_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(Config.ACCESS_TOKEN_EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

# decode JWT
def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

# role-based authentication
def role_required(role):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith("Bearer"):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(" ")[1]  
            payload = decode_jwt_token(token)

            if 'error' in payload:
                return jsonify(payload), 401

            if payload['role'] != role:
                return jsonify({"error": "Unauthorized access"}), 403

            request.user_id = payload['user_id']
            request.role = payload['role']
            return fn(*args, **kwargs)

        decorator.__name__ = fn.__name__
        return decorator
    return wrapper


#------------------------------Admin Part-------------------------------------------

# Admin login 
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD_HASH = generate_password_hash('admin123')

    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        token = create_jwt_token(user_id=0, role='admin')  # Admin ID is 0
        return jsonify({"message": "Admin login successful", "authToken": token, "redirect": "/admin/dashboard"})
    return jsonify({"message": "Invalid admin credentials"}), 401

#Admin Dashboard routes
@app.route('/admin/dashboard', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=30) 
def admin_dashboard():
    print("this is admin dashboard")
    return jsonify({"message": "Welcome to Admin Dashboard"})


# route for admin to see all the users
@app.route('/admin/manageusers', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=30)
def manageusers_():
    users = User.query.all()
    data = [
        {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            "block": user.block
        } for user in users  
    ]
    
    current_time = datetime.now().time()

    print(f"manageusers_ API called at {current_time}")
    return jsonify(data)

#Routes for admin to block the user
@app.route('/admin/block_user/<int:user_id>', methods=['POST'])
@role_required('admin')
def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.block = not user.block
    db.session.commit()
    cache.clear()
    return jsonify({"message": "User status updated successfully"}), 200


# route for admin to get the unverified professionals
@app.route('/admin/unverified-professionals', methods=['GET'])
@role_required('admin') 
# @cache.cached(timeout=30)
def get_unverified_professionals():
    professionals = ServiceProfessional.query.filter_by(verified=False).all()
    data = [
        {
            "id": p.id,
            "name": p.user.username,
            "experience": p.experience,
            "skills": p.skills,
            "service" : p.service.name,
            "phone": p.phone,
            "address": p.address,
            "pin_code": p.pin_code
        } for p in professionals
    ]
    return jsonify(data)

#routes for admin to verify the professional
@app.route('/admin/verify-professional/<int:professional_id>', methods=['POST'])
@role_required('admin')
def verify_professional(professional_id):
    professional = ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    if professional.verified:
        return jsonify({"message": "Professional already verified"}), 400

    professional.verified = True
    db.session.commit()
    # cache.clear()
    return jsonify({"message": "Professional verified successfully"}), 200


#route for admin to get the verified professionals 
@app.route('/admin/verified-professionals', methods=['GET'])
# @cache.cached(timeout=30)
@role_required('admin')
def get_verified_professionals():
    professionals = ServiceProfessional.query.filter_by(verified=True).all()
    data = [
        {
            "id": p.id,
            "name": p.user.username,
            "experience": p.experience,
            "service" : p.service.name,
            "skills": p.skills,
            "phone": p.phone,
            "address": p.address,
            "pin_code": p.pin_code
        } for p in professionals
    ]
    return jsonify(data)


#routes for admin to unverify the professionals 
@app.route('/admin/unverify-professional/<int:professional_id>', methods=['POST'])
@role_required('admin')
def unverify_professional(professional_id):
    professional = ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    if not professional.verified:
        return jsonify({"error": "Professional is already unverified"}), 400

    professional.verified = False
    db.session.commit()
    # cache.clear()
    return jsonify({"message": "Professional unverified successfully"}), 200



# route for getting existing service types 
@app.route('/get_existing_service_types', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=30)
def get_existing_service_types():
    service_types = ServiceType.query.all()
    data = [
        {
            "id": st.id,
            "name": st.name,
            "description": st.description
        } for st in service_types
    ]
    return jsonify(data)


# route for creating new service types
@app.route('/create_new_service_type', methods=['POST'])
@role_required('admin')
def create_new_service_type():
    data = request.json
    name = data['name']
    description = data['description']

    if ServiceType.query.filter_by(name=name).first():
        return jsonify({"error": "Service type already exists"}), 200

    new_service_type = ServiceType(name=name, description=description)
    db.session.add(new_service_type)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Service type created successfully"}), 201


# route for getting existing services
@app.route('/get_existing_services', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=30)
def get_existing_services():
    services = Service.query.all()
    services_data = [
        {
            "id": service.id,
            "service_name": service.name,
            "service_type": service.service_type.name,
            "service_description": service.description,
            "price": service.base_price,
            'service_type_id': service.service_type_id
        }
        for service in services
    ]
    return jsonify(services_data)

# route for creating new services
@app.route('/admin/create_new_service', methods=['POST'])
@role_required('admin')
def create_new_service():
    data = request.json
    print(data)  
    service_name = data.get('service_name')
    service_description = data.get('service_description')
    price = data.get('price')
    service_type_id = data.get('service_type_id')

    existing_service = Service.query.filter(Service.name == service_name).first()
    if existing_service:
        return jsonify({"error": "Service already exists"}), 200

    new_service = Service(name=service_name, description=service_description, base_price=price, service_type_id=service_type_id)
    db.session.add(new_service)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Service created successfully"}), 200


# route for editing service type
@app.route('/edit_service_type/<service_type_id>', methods=['PUT'])
@role_required('admin')
def edit_service_type(service_type_id):
    data = request.json
    service_type = ServiceType.query.get(service_type_id)
    if not service_type:
        return jsonify({"error": "Service type not found"}), 404
    
    service_type.name = data.get('name', service_type.name)
    service_type.description = data.get('description', service_type.description)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Service type updated successfully"}), 200
#route for deleting service type
@app.route('/delete_service_type/<service_type_id>', methods=['DELETE'])
@role_required('admin')
def delete_service_type(service_type_id):
    service_type = ServiceType.query.get(service_type_id)
    if not service_type:
        return jsonify({"error": "Service type not found"}), 404
    if not service_type.services:
        db.session.delete(service_type)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Service type deleted successfully"}), 200
    return jsonify({"error": "Cannot delete service type with associated services"}),400
    
#route for editing service 
@app.route('/edit_service/<service_id>', methods=['PUT'])
@role_required('admin')
def edit_service(service_id):
    data = request.json
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    service.name = data.get('service_name', service.name)
    service.description = data.get('service_description', service.description)
    service.base_price = data.get('price', service.base_price)
    service.service_type_id = data.get('service_type_id', service.service_type_id)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Service updated successfully"}), 200

# route for deleting service 
@app.route('/delete_service/<service_id>', methods=['DELETE'])
@role_required('admin')
def delete_service(service_id):
    service = Service.query.get(service_id)
    print(service)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    if not service.serviceprofessionals:
        db.session.delete(service)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Service deleted successfully"}), 200

    print(service.serviceprofessionals.user.name)
    # db.session.delete(service)
    # db.session.commit()
    return jsonify({"error": "Service can not be deleted as it is booked by the customer or alloted to the service professional"}), 400


#route for admin to get all the professional
@app.route('/professionals', methods=['GET'])
@role_required('admin') 
def get_professionals():
    """Get all professionals."""
    professionals = ServiceProfessional.query.all()
    result = []
    for professional in professionals:
        result.append({
            "id": professional.id,
            "user_id": professional.user_id,
            "experience":professional.experience,
            "service_id": professional.service_id,
            "verified": professional.verified,
            

        })
    return jsonify(result)



@app.route('/admin/user_details/<int:user_id>', methods=['GET'])
@role_required('admin')
# @cache.cached(timeout=300)  
def get_user_details(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    professional_id = user.professional.id if user.professional else None

    print(f"this is result {user.name}")
  
    requests = ServiceRequest.query.filter_by(professional_id = professional_id).all()
    reviews = [{'rating': req.rating, 'review': req.review} for req in requests if req.rating is not None]

    average_rating = None
    if reviews:
        total_rating = sum([r['rating'] for r in reviews])
        average_rating = round(total_rating / len(reviews), 2)


    user_details = {
        'role': user.role,
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'phone': getattr(user.professional, 'phone', ''),
        'address': getattr(user.professional, 'address', ''),
        'pin_code': getattr(user.professional, 'pin_code', ''),
        'average_rating': average_rating,
        'reviews': reviews,
    }

    print(f"User details fetched: {user_details}")  
    return jsonify(user_details)


#route for admin search professional

@app.route('/admin/search_professionals', methods=['GET'])
@role_required('admin')
# @cache.cached(timeout=300)
def search_professionals():
    query = request.args.get('query', '').lower()

    if not query:
        return jsonify({"message": "Search query is missing"}), 400

    # Join related models for search
    results = db.session.query(ServiceProfessional)\
        .join(User)\
        .join(Service)\
        .outerjoin(ServiceRequest)\
        .filter(
            or_(
                User.name.ilike(f"%{query}%"),
                Service.name.ilike(f"%{query}%"),
                ServiceRequest.review.ilike(f"%{query}%"),
                ServiceRequest.rating.ilike(f"%{query}%")
            )
        ).options(
            joinedload(ServiceProfessional.user),
            joinedload(ServiceProfessional.service)
        ).all()

    professionals = [
        {
            "id": prof.id,
            "name": prof.user.name,
            "username": prof.user.username,
            "email": prof.user.email,
            "service_name": prof.service.name,
            "rating": avg_rating(prof.requests), 
            "review_count": len(prof.requests),
            "block": prof.user.block,
        }
        for prof in results
    ]
    return jsonify(professionals)

# Helper Function
def avg_rating(requests):
    ratings = [req.rating for req in requests if req.rating is not None]
    return sum(ratings) / len(ratings) if ratings else None


@app.route('/admin_chart', methods=['GET'])
@role_required('admin')
def admin_chart():
    services = Service.query.all()
    service_counts = {}

    for service in services:
        service_counts[service.name] = ServiceRequest.query.filter_by(service_id=service.id).count()
    result = {
        "labels": list(service_counts.keys()),  
        "data": list(service_counts.values())   
    }
    
    return jsonify(result),200



@app.route('/admin_service_req', methods=['GET'])
@role_required('admin')
def admin_service_req():
    # user_id = request.user_id  
    # print("User ID:", user_id)
    status_counts = (
        db.session.query(ServiceRequest.service_status, func.count(ServiceRequest.id))
        .group_by(ServiceRequest.service_status)
        .all()
    )
    statuses = ['requested', 'assigned', 'closed', 'rejected']
    counts = {status: 0 for status in statuses}
    for status, count in status_counts:
        counts[status] = count
    return jsonify({
        'labels': statuses,
        'counts': [counts['requested'], counts['assigned'], counts['closed'], counts['rejected']]
    }), 200
   


@app.route('/admin_all_services_requests', methods=['GET'])
@role_required('admin')
def admin_all_services_requests():
    service_requests = ServiceRequest.query.all()
    result = []
    for req in service_requests:
        customer = User.query.filter_by(id=req.customer_id).first()
        result.append({
            "id": req.id,
            "service_name": req.service.name,
            "professional_name": req.professional.user.name,
            "customer_name": customer.name,
            "date_of_request": req.date_of_request,
            "service_status": req.service_status,
            "date_of_completion": req.date_of_completion,
        })
    return jsonify(result)


#------------------------------Login and Regidter Part-----------------------------------------

# Professional and Customer Registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    existing_user = User.query.filter(
        or_(User.username == data['username'], User.email == data['email'])
    ).first()
    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        name = data['name'],
        email=data['email'],
        password=hashed_password,
        role=data['role'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    # Handle professional registration
    if data['role'] == 'professional':
        selected_service = Service.query.get(data['service_id'])
        if not selected_service :
            return jsonify({'message': 'Invalid service entered'}), 400

        new_professional = ServiceProfessional(
            user_id=new_user.id,
            experience=data.get('experience', 0),
            service_id=selected_service.id,  
            phone=data['phone'],
            address=data['address'],
            pin_code=data['pin_code'],
            verified=False
        )
        db.session.add(new_professional)
        db.session.commit()
        return jsonify({'message': 'Registration pending, Admin approval required.'}), 201

    # Handle customer registration
    elif data['role'] == 'customer':
        new_customer = Customer(
            user_id=new_user.id,
            phone=data['phone'],
            address=data['address'],
            pin_code=data['pin_code']
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer registration successful.'}), 201

    return jsonify({'message': 'Invalid role selected'}), 400

# getting services for registering new professional
@app.route('/get_services')

def get_services():
    services = Service.query.all()
    service_data = [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.base_price
        } for service in services
    ]
    return jsonify(service_data)
    

# Login for customer and professional
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('username')  
    password = data.get('password')

    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()
    if user and check_password_hash(user.password, password):
        if user.block == True:
            return jsonify({"message": "Your account has been blocked"}), 200
        if user.role == 'professional':
            professional = ServiceProfessional.query.filter_by(user_id=user.id).first()
            if not professional or not professional.verified :
                return jsonify({"message": "Your account is pending admin approval"}), 200

        # token = create_jwt_token(user_id=user.id, role=user.role)
        if user.role == 'professional':
             token = create_jwt_token(user_id=user.id, role=user.role)  
             return jsonify({"message": "Login successful", "role": user.role, "authToken": token, "redirect": "/professional/dashboard"}),200
        if user.role == 'customer':
             token = create_jwt_token(user_id=user.id, role=user.role)
             return jsonify({"message": "Login successful", "role": user.role, "authToken": token, "redirect": "/customer/dashboard"}),200

    return jsonify({"message": "Invalid username or password"}), 200


#------------------------------Customer Part-------------------------------------------


@app.route('/customer/dashboard', methods=['GET'])
@role_required('customer')
def customer_dashboard():
    cid = request.user_id
    user = User.query.filter_by(id=cid).first()
    return jsonify({"message": f"Welcome {user.name} to Customer Dashboard"})

# route for customer to get all available service types
@app.route('/service_types_', methods=['GET'])
@role_required('customer') 
# @cache.cached(timeout=300)
def service_types_():
    """Get all service types."""
    service_types = ServiceType.query.all()
    result = []
    for service_type in service_types:
        result.append({
            "id": service_type.id,
            "name": service_type.name,
            "description": service_type.description
        })
    return jsonify(result)

#route for customer to get all available services 
@app.route('/services_', methods=['GET'])
@role_required('customer')  
# @cache.cached(timeout=300)
def get_services_():
    print("there are services")
    service_type_id = request.args.get('service_type_id')
    # service_type_id= 1
    print(f"service_type_id: {service_type_id}")
    query = Service.query
    if service_type_id:
        query = query.filter(Service.service_type_id == service_type_id)
    services = query.all()

    result = []
    for service in services:
        result.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
            "service_type": {
                "id": service.service_type.id,
                "name": service.service_type.name
            }
        })
    print(result)
    return jsonify(result)


#route for customer to get all available professional for a particular service
@app.route('/service/<int:service_id>/professionals', methods=['GET'])
@role_required('customer')  
# @cache.cached(timeout=300)
def get_service_professionals(service_id):
    print(f"service_id: {service_id}")
    """Get all professionals offering a specific service, ordered by average rating."""
    try:
        professionals_with_ratings = db.session.query(
            ServiceProfessional.id,
            User.username,
            User.name,
            ServiceProfessional.experience,
            Service.name.label('service_name'),
            ServiceProfessional.phone,
            ServiceProfessional.address,
            ServiceProfessional.pin_code,
            func.avg(ServiceRequest.rating).label('average_rating')
        ).join(User, ServiceProfessional.user_id == User.id)\
         .join(Service, ServiceProfessional.service_id == Service.id)\
         .outerjoin(ServiceRequest, ServiceProfessional.id == ServiceRequest.professional_id)\
         .filter(
             and_(
                 ServiceProfessional.service_id == service_id,
                 ServiceProfessional.verified == True,
                 User.block == False
             )
         ).group_by(
             ServiceProfessional.id, User.username,User.name, ServiceProfessional.experience,
             Service.name, ServiceProfessional.phone,
             ServiceProfessional.address, ServiceProfessional.pin_code
         ).order_by(func.avg(ServiceRequest.rating).desc())\
         .all()
        print(f"Professionals with ratings: {professionals_with_ratings}")
        if not professionals_with_ratings:
            return jsonify([])
        result = []
        for professional in professionals_with_ratings:
            result.append({
                "id": professional.id,
                "name": professional.name,
                "Professional_username": professional.username,
                "experience": professional.experience,
                "service": professional.service_name,
                "phone": professional.phone,
                "address": professional.address,
                "pin_code": professional.pin_code,
                "average_rating": round(professional.average_rating, 2) if professional.average_rating else 0.0
            })
        print(f"this is result: %s" % result)
        return jsonify(result)

    except Exception as e:
        print(f"Error fetching professionals: {e}")
        return jsonify({"error": "Failed to fetch professionals"}), 500


# route for customer to book service 
@app.route('/service_request', methods=['POST'])
@role_required('customer') 
def book_service():
    print("book service")
    customer_id = request.user_id
    print(f"customer_id: {customer_id}")
    data = request.json

    new_request = ServiceRequest(
        professional_id = data['professional_id'],
        service_id=data['service_id'],
        customer_id=customer_id, 
        # date_of_request = datetime.utcnow(),
        date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d')
        # remarks=data.get('remarks') 
        
    )
    print(datetime.strptime(data['date_of_request'], '%Y-%m-%d'))
    req = ServiceRequest.query.filter_by (service_id=data['service_id'], customer_id=customer_id ).all()
    if req:
      for r in req:
        print(r.service_status)
        if r.service_status == 'requested' or r.service_status == 'assigned':
             return jsonify({"message": "You have already requested this service."}), 200
        # if r.service_status == 'rejected':
        #      return jsonify({"message": "This professional has rejected the service request."}), 400
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Service booked successfully!"}), 201


#routes for customer to see the service request made by him
@app.route('/customer/service_requests', methods=['GET'])
@role_required('customer') 
# @cache.cached(timeout=300)
def get_customer_service_requests():
    """Get all service requests for the logged-in customer."""
    customer_id = request.user_id
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    result = []
    for req in service_requests:
        result.append({
            "id": req.id,
            "service_id":req.service_id,
            "service_name": req.service.name,
            "professional_name": req.professional.user.name,
            "date_of_request": req.date_time_of_service,
            "date_of_appointment": req.date_of_request,
            "date_of_completion": req.date_of_completion,
            "service_status": req.service_status
        })
    return jsonify(result)


#route for customer to change the status of the requested services 
@app.route('/customer/service_requests/<int:request_id>', methods=['PUT'])
@role_required('customer')
def close_service_request(request_id):
    user_id = request.user_id  
    data = request.json
    review = data.get('review')
    rating = data.get('rating')
    if not review or not rating:
        return jsonify({"message": "Review and rating are required."}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"message": "Rating must be between 1 and 5."}), 400
    except ValueError:
        return jsonify({"message": "Invalid rating."}), 400

    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=user_id).first()
    if not service_request:
        return jsonify({"message": "Service request not found."}), 404
    if service_request.service_status != 'assigned':
        return jsonify({"message": "Only assigned services can be closed."}), 400

    service_request.service_status = 'closed'
    service_request.review = review
    service_request.rating = rating
    service_request.date_of_completion = datetime.utcnow()

    db.session.commit()
    # cache.clear()
    return jsonify({"message": "Service request closed successfully."}), 200

#route to edit the request
@app.route('/customer/edit_service_requests/<int:request_id>', methods=['PUT'])
@role_required('customer')
def update_service_request2(request_id):
    """Update a service request."""
    data = request.json
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.customer_id != request.user_id:
        return jsonify({"message": "Unauthorized"}), 403
    print("this is ",data) 
    if service_request.service_status != 'requested':
        return jsonify({"message": "Cannot edit this service request."}), 403

    try:
      service_request.date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d')
    except KeyError:
      return {"error": "Missing 'date_of_request' field"}, 400
    except ValueError as e:
      return {"error": f"Invalid date format: {str(e)}"}, 400

    service_request.professional_id = data['professional_id']
    db.session.commit()
    # cache.clear()
    return jsonify({"message": "Service request updated cessfully!"})

#route to delete the service request
@app.route('/customer/delete_service_requests/<int:request_id>', methods=['DELETE'])
@role_required('customer')
def delete_service_request(request_id):
    try:
        user_id = request.user_id
        service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=user_id).first()

        if not service_request:
            return jsonify({"error": "Service request not found or unauthorized."}), 404

        if service_request.service_status not in ["requested", "rejected"]:
            return jsonify({"error": "Cannot delete this service request."}), 400

        db.session.delete(service_request)
        db.session.commit()
        # cache.clear()

        return jsonify({"message": "Service request deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 

#Search service for the customer 

@app.route('/search-services', methods=['GET'])
@role_required('customer')
def search_services():
    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        return jsonify({"services": []}) 

    results = (
        db.session.query(Service, ServiceProfessional)
        .join(ServiceProfessional, Service.id == ServiceProfessional.service_id)
        .filter(
            or_(
                Service.name.ilike(f"%{keyword}%"),  
                ServiceProfessional.address.ilike(f"%{keyword}%"),  
                ServiceProfessional.pin_code.ilike(f"%{keyword}%")
            )
        )
        .all()
    )

    # Serialize results
    services = []
    for service, professional in results:
        services.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
            "professional": {
                "id": professional.id if professional else None,
                "name": professional.user.name if professional and professional.user else None,
                "address": professional.address if professional else None,
                "pin_code": professional.pin_code if professional else None,
                "experience": professional.experience if professional else None,
            },
        })

    return jsonify({"services": services})

#Customer Chart
@app.route('/customer_summary', methods=['GET'])
@role_required('customer')
def service_status_chart():
    user_id = request.user_id 
    print("User ID:", user_id)
    status_counts = (
        db.session.query(ServiceRequest.service_status, func.count(ServiceRequest.id))
        .filter(ServiceRequest.customer_id == user_id)
        .group_by(ServiceRequest.service_status)
        .all()
    )
    statuses = ['requested', 'assigned', 'closed', 'rejected']
    counts = {status: 0 for status in statuses}
    for status, count in status_counts:
        counts[status] = count
    return jsonify({
        'labels': statuses,
        'counts': [counts['requested'], counts['assigned'], counts['closed'], counts['rejected']]
    }), 200


#------------------------------Professional Part-------------------------------------------


@app.route('/professional/dashboard', methods=['GET'])
@role_required('professional')
def professional_dashboard():
     professional_i = request.user_id
     user = User.query.filter_by(id=professional_i).first()
     return jsonify({f"message": f"Welcome {user.name} to Professionals Dashboard"})


# route for professional to get the service requests
@app.route('/service_requests_for_professionals', methods=['GET'])
@role_required('professional')
# @cache.cached(timeout=300)
def get_service_requests_for_professionals():
    professional_i = request.user_id
    pro = ServiceProfessional.query.filter_by(user_id=professional_i).first()
    print(f"this is professional_id {pro.id}")
    service_requests = ServiceRequest.query.filter_by(professional_id=pro.id).all()
    result = []
    for req in service_requests:
        customer_name = User.query.filter_by(id=req.customer_id).first()
        customer_details = Customer.query.filter_by(user_id=customer_name.id).first()
        result.append({
            "id": req.id,
            "service_name": req.service.name,
            "customer_name": customer_name.name,
            "customer_contact_number": customer_details.phone,
            "customer_address": customer_details.address,
            "customer_pin_code": customer_details.pin_code,
            "date_of_request": req.date_of_request,
            "service_status": req.service_status,
            "rating": req.rating,
            "review": req.review,
            "date_of_completion": req.date_of_completion,
        })
    print(f"this is result {result}")
    print(professional_i)
    return jsonify(result)

# route for professional to update the status of the service requests
@app.route('/professional/service_requests/<int:service_id>', methods=['PUT'])
@role_required('professional')
def update_service_request1(service_id):
    data = request.get_json()
    service_status = data.get('service_status')

    if service_status not in ['assigned', 'rejected']:
        return jsonify({'message': 'Invalid data. Service status must be "assigned" or "rejected".'}), 400

    service_request = ServiceRequest.query.get(service_id)
    if not service_request:
        return jsonify({'message': 'Service request not found.'}), 404
    if service_request.service_status != 'requested':
        return jsonify({'message': 'Service request is not in a "requested" state.'}), 400
    service_request.service_status = service_status

    try:
        db.session.commit()
        # cache.clear()
        return jsonify({
            'message': f'Service request updated successfully to {service_status}.',
            'service_request': {
                'id': service_request.id,
                'service_name': service_request.service.name,  
                'customer_name': service_request.user.username,  
                'service_status': service_request.service_status,
                'date_of_request': service_request.date_of_request.strftime('%Y-%m-%d'),
                'date_of_completion': service_request.date_of_completion.strftime('%Y-%m-%d') if service_request.date_of_completion else None,
            }
        }), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Failed to update service request.', 'error': str(e)}), 500

@app.route('/closed_service', methods=['GET'])
@role_required('professional')
def get_closed_service_requests():
    professional_i = request.user_id
    pro = ServiceProfessional.query.filter_by(user_id=professional_i).first()
    closed_requests = ServiceRequest.query.filter_by(professional_id=pro.id, service_status='closed').all()
    result = []
    for req in closed_requests:
        customer_name = User.query.filter_by(id=req.customer_id).first()
        customer_details = Customer.query.filter_by(user_id=customer_name.id).first()
        result.append({
            "id": req.id,
            "service_name": req.service.name,
            "customer_name": customer_name.name,
            "customer_contact_number": customer_details.phone,
            "customer_address": customer_details.address,
            "customer_pin_code": customer_details.pin_code,
            "date_of_request": req.date_of_request,
            "service_status": req.service_status,
            "rating": req.rating,
            "review": req.review,
            "date_of_completion": req.date_of_completion,
        })
    return jsonify(result)
    



#---------------------------------------Export CSV---------------------------------------

@app.get('/export_csv')
def export_csv():
    task = export_service_requests_task.delay()
    return jsonify({ 'task_id':task.id})

@app.get('/get_export_csv/<id>')
def get_export_csv(id):
    res = AsyncResult(id)
    print(f"this is res  {res}")
    try:
        if res.ready():
            return send_file(f"aman_export_csv/admin_{res}.csv")
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"message": "Task is still running"}) 


#-----------------------------------------Logout Part--------------------------------------------


# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({"message": "Logged out successfully"})
