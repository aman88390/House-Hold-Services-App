
# # celeryconfig.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'Asia/Kolkata'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
