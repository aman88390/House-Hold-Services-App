
from celery import shared_task
from application.model import User, ServiceType, Service, ServiceProfessional, ServiceRequest, Customer
from datetime import datetime, timedelta
import pytz
from jinja2 import Template
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .worker import celery  
import flask_excel
from sqlalchemy.orm import load_only

import os
import csv
from flask import current_app
from .model import ServiceRequest  



SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = '21f3003230@ds.study.iitm.ac.in'
SENDER_PASSWORD = 'eyglqcrgnfxjgelk'

def send_email(to, subject, content_body):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["To"] = to
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg.attach(MIMEText(content_body, 'html')) 

       
        client = SMTP(SMTP_HOST, SMTP_PORT)
        client.ehlo()  
        client.starttls()  
        client.ehlo()  
        client.login(SENDER_EMAIL, SENDER_PASSWORD)

        client.send_message(msg)
        print(f"Email sent to {to} successfully!")

        client.quit()

    except Exception as e:
        print(f"Error sending email to {to}: {e}")
        raise

IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    return datetime.now(IST)

@shared_task(ignore_result=True)
def daily_reminder_for_professionals():
    template = '''
    <p>Dear {{ professional_name }},</p>
    <p>You have a pending service request that needs your attention.</p>
    <p>Service: {{ service_name }}</p>
    <p>Please visit or accept/reject the service request.</p>
    <p>Thank you for your prompt action.</p>
    <br />
    <p>Best Regards,</p>
    <p>Your Service Team</p>
    '''

    timestamp = datetime.now(IST) - timedelta(minutes=1)

    pending_requests = ServiceRequest.query.filter(
        ServiceRequest.service_status == 'requested',
        ServiceRequest.date_of_request < timestamp
    ).all()

    professionals_with_pending_requests = {}

    for request in pending_requests:
        professional = ServiceProfessional.query.filter_by(id=request.professional_id).first()
        if professional:
            if professional.id not in professionals_with_pending_requests:
                professionals_with_pending_requests[professional.id] = []

            professionals_with_pending_requests[professional.id].append(request)

    for professional_id, requests in professionals_with_pending_requests.items():
        professional = ServiceProfessional.query.filter_by(id=professional_id).first()
        if professional:
            user = User.query.filter_by(id=professional.user_id).first()
            if user and user.email:
                subject = f"Reminder: You have pending service requests"
                service_names = [request.service.name for request in requests]
                content = Template(template).render(
                    professional_name=user.username,
                    service_name=", ".join(service_names)
                )

                send_email(user.email, subject, content)


def get_month_range():
    today = datetime.now(IST)
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return first_day, last_day

@shared_task(ignore_result=True)
def send_monthly_activity_report():
    template= '''
<html>
    <body>
        <h2>Monthly Activity Report - {{ customer_name }}</h2>
        <p>Dear {{ customer_name }},</p>
        <p>Here is the summary of your activity for the month:</p>
        <table border="1">
            <thead>
                <tr>
                    <th>Service Status</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Requested</td>
                    <td>{{ requested }}</td>
                </tr>
                <tr>
                    <td>Assigned</td>
                    <td>{{ assigned }}</td>
                </tr>
                <tr>
                    <td>Closed</td>
                    <td>{{ closed }}</td>
                </tr>
                <tr>
                    <td>Rejected</td>
                    <td>{{ rejected }}</td>
                </tr>
            </tbody>
        </table>
        <br />
        <p>Thank you for using our service!</p>
        <p>Best regards, <br />Your Service Team</p>
    </body>
</html>
'''
    template = Template(template)
    first_day, last_day = get_month_range()

    customers = User.query.filter(User.role == 'customer').all()
    for customer in customers:

        requests = ServiceRequest.query.filter(
            ServiceRequest.customer_id == customer.id,
            ServiceRequest.date_of_request >= first_day,
            ServiceRequest.date_of_request <= last_day
        ).all()

    
        requested = len(requests)
        assigned = sum(1 for req in requests if req.service_status == 'assigned')
        closed = sum(1 for req in requests if req.service_status == 'closed')
        rejected = sum(1 for req in requests if req.service_status == 'rejected')

        subject = "Monthly Service Activity Report"
        report_html = template.render(
            customer_name=customer.name,
            requested=requested,
            assigned=assigned,
            closed=closed,
            rejected=rejected
        )

        send_email(customer.email, subject, report_html)





@shared_task(bind=True, ignore_result=False)
def export_service_requests_task(self):

    try:
        service_requests = ServiceRequest.query.filter(
            ServiceRequest.service_status == 'closed'
        ).all()

        if not service_requests:
            raise ValueError("No closed service requests found.")

        task_id = self.request.id
        csv_name = f"admin_{task_id}.csv"
        export_dir = 'aman_export_csv'
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, csv_name)
        column_names = [column.name for column in ServiceRequest.__table__.columns]
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  
            for request in service_requests:
                writer.writerow([getattr(request, col) for col in column_names])  

        current_app.logger.info(f"Exported CSV successfully: {file_path}")
        return csv_name

    except Exception as e:
        current_app.logger.error(f"Error exporting service requests: {e}")
        raise RuntimeError("Failed to export service requests to CSV") from e


