from __future__ import unicode_literals
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

from apps.canvas_gadget.views import DeployView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^payments/", include("pinax.stripe.urls")),
    url(r'^projects/', include('apps.projects.urls', namespace="projects")),
    url(r'^demobooth/', include('apps.demobooth.urls', namespace="demobooth")),
    
    url(r'^api/', include('apps.api.urls', namespace="api")),
    url(r'^deploy/$', DeployView.as_view(), name='deploy_view'),
    
     url(r'seesoon/', include('apps.seesoon.urls', namespace="seesoon")),
#     url(r'(.*)/', include('apps.seesoon.urls')),
#     url(r'', include('apps.seesoon.urls')),
    
    url(r'', include('apps.canvas_gadget.urls', namespace="canvas_gadget")),
    url(r'', include('apps.accounts.urls', namespace="accounts")),
    url(r'feedback/', include('apps.feedback.urls', namespace="feedback")),
    
    url(r'^billing/', include('apps.billing.urls', namespace="billing")),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^google4e6aebbbfad69b51\.html$', lambda r: HttpResponse("google-site-verification: google4e6aebbbfad69b51.html", content_type="text/plain")),

]

if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(
#         url(r'^__debug__/', include(debug_toolbar.urls))
#     )
    
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

