from django.contrib import admin
from django.urls import path, include
from api import urls
from api.views.frontend import Frontend
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from backend import views
admin.autodiscover()

urlpatterns = [
    path('', Frontend.as_view()),
    path('admin/', admin.site.urls),
    path('deploy/', views.deploy),
    path('api/', include(urls)),
    path('docs/', RedirectView.as_view(url='/docs/index.html'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.DOCS_URL, document_root=settings.DOCS_ROOT)
