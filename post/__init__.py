from django.apps import AppConfig

class PostAppConfig(AppConfig):
    name = 'post'
    label = 'post'
    verbose_name = 'Post'

    def ready(self):
        import post.signals

default_app_config = 'post.PostAppConfig'