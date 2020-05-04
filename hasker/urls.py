from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from hasker import settings

urlpatterns = [
                  path("account/", include("account.urls")),
                  path("admin/", admin.site.urls),
                  path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path("", include("question_and_answer.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


if settings.URL_PREFIX_TO_CHECK_SENTRY:
    urlpatterns += [
        path(f"sentry-debug-{settings.URL_PREFIX_TO_CHECK_SENTRY}/", trigger_error),
    ]

schema_view = get_schema_view(
    openapi.Info(
        title="Hasker api",
        default_version='v1',
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns += [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
