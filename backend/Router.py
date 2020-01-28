# src: https://docs.djangoproject.com/en/2.0/topics/db/multi-db/
class AppRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api':
            return 'api_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'api':
            return 'api_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'api' or \
           obj2._meta.app_label == 'api':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'api':
            return db == 'api_db'
        return db == 'default'