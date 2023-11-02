from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserProfileView, UserCreateViewSet
from .entries.views import EntryListViewSet, EntryCreateView, EntryDetailViewSet

router = DefaultRouter()
router.register(r'register', UserCreateViewSet)
router.register(r'entries', EntryListViewSet)
router.register(r'entries', EntryDetailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/profile/', UserProfileView.as_view()),
    path('api/v1/entries/create/', EntryCreateView.as_view()),

    path('api/v1/', include(router.urls)),

    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
