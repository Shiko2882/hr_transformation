from django.apps import AppConfig


class HrAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hr_admin'

    def ready(self):
        import hr_admin.signals
