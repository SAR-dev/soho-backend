from django.conf import settings # import the settings file

def frontend_url(request):
    return {'FRONTEND_URL': settings.FRONTEND_URL}