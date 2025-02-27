from django.apps import AppConfig


class HiringmanagementtoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hiringManagementTool'

    def ready(self):
        from hiringManagementTool.components.demands import signals