from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from .users.views import UserProfileView, UserCreateView
from .entries.views import EntryListViewSet, EntryCreateView, EntryDetailViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
        contact=openapi.Contact(email="herciliomartins@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


router = DefaultRouter()
router.register(r'entries', EntryDetailViewSet)
router.register(r'entries', EntryListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/register/', UserCreateView.as_view(), name='user-create'),
    path('api/v1/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/v1/entries/create/', EntryCreateView.as_view(), name='entry-create'),

    path('api/v1/', include(router.urls)),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
