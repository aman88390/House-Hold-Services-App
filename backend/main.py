from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app1 import app as app_blueprint  
from config import Config
from application.model import db
from extensions import cache 
from flask_migrate import Migrate
from application.tasks import daily_reminder_for_professionals, send_monthly_activity_report
from application.worker import celery_init_app  
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)
    jwt = JWTManager(app)
    Migrate().init_app(app, db)

    app.register_blueprint(app_blueprint)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
celery_app = celery_init_app(app) 
from celery.schedules import crontab

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(minute=0, hour=10),
    #                          daily_reminder_for_professionals.s(),)

    sender.add_periodic_task(
        crontab(minute='*'),  # '*' means every minute
        daily_reminder_for_professionals.s(),)
    # sender.add_periodic_task(
    #     crontab(minute=0, hour=12, day_of_month=1),
    #     send_monthly_activity_report.s()  
    sender.add_periodic_task(crontab(minute='*'), send_monthly_activity_report.s(),
     )  
   

if __name__ == '__main__':
    app.run(debug=True)

 
