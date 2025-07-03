# # application/__init__.py

# from flask import Flask
# from .worker import create_celery 
# from .tasks import daily_reminder_for_professionals # Import the create_celery function

# def create_app():
#     app = Flask(__name__)
#     # Other app initialization code here...
    
#     # Initialize Celery with the app
#     celery = create_celery(app)
#     app.celery = celery  # Store the celery instance on the app object

#     return app

# # Create a Celery instance directly for the command
# celery = create_celery(create_app())
