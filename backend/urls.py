from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('docs/', include_docs_urls(title='DRF API')),
    path('admin/', admin.site.urls),
    # path('api/auth/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/auth/', include('djoser.social.urls')),
    # path('api/auth/', include('trench.urls')), # Base endpoints
    # path('api/auth/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/auth/', include('trench.urls.djoser')),  # for Token Based Authorization
    path('api/account/', include('account.urls', namespace='account')),
    path('api/group/', include('group.urls', namespace='group')),
    path('api/post/', include('post.urls', namespace='post')),
    path('api/image/', include('image.urls', namespace='image')),
    path('api/choice/', include('choice.urls', namespace='choice')),
    path('api/comment/', include('comment.urls', namespace='comment')),
    path('api/moderator/', include('moderator.urls', namespace='moderator')),
    path('api/award/', include('award.urls', namespace='award')),
    path('api/activity/', include('activity.urls', namespace='activity')),
    path('api/advertisement/', include('advertisement.urls', namespace='advertisement')),
    # path('api/warning/', include('warning.urls', namespace='warning')),
    # path('api/contact/', include('contact.urls', namespace='contact')),
    path('api/payment/', include('payment.urls', namespace='payment')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
