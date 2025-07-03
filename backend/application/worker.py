from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.import_name, task_cls=FlaskTask)
    celery_app.config_from_object("celeryconfig")  
    return celery_app
celery = None

def create_celery(app):
    global celery
    if not celery:
        celery = celery_init_app(app)
    return celery
