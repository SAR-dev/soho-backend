from django.apps import AppConfig

class CommentAppConfig(AppConfig):
    name = 'comment'
    label = 'comment'
    verbose_name = 'Comment'

    def ready(self):
        import comment.signals

default_app_config = 'comment.CommentAppConfig'