from django.apps import AppConfig

class GroupAppConfig(AppConfig):
    name = 'group'
    label = 'group'
    verbose_name = 'Group'

    def ready(self):
        import group.signals

default_app_config = 'group.GroupAppConfig'