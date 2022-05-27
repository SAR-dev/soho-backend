from django.apps import AppConfig

class AccountAppConfig(AppConfig):
    name = 'account'
    label = 'account'
    verbose_name = 'Account'

    def ready(self):
        import account.signals

default_app_config = 'account.AccountAppConfig'