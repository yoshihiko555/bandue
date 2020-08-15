from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.views.generic import TemplateView

from rest_framework_jwt.views import obtain_jwt_token

from . import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token),
    # path('', include('front_view.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('<path:path>', TemplateView.as_view(template_name='index.html'))]
