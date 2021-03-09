from api import views as api_views
from auth0login.views import logout
from core import views as core_views
from django.contrib import admin
from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path("", core_views.index),
    path("healthcheck", core_views.healthcheck),
    path("logout", logout),
    path("api/submitReport", api_views.submit_report),
    path("api/submitReport/debug", api_views.submit_report_debug),
    path("api/requestCall", api_views.request_call),
    path("api/requestCall/debug", api_views.request_call_debug),
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    path("admin/docs/", lambda r: redirect("/admin/docs/models/", permanent=False)),
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path(
        "admin/core/callreport/",
        lambda r: HttpResponsePermanentRedirect("/admin/core/report/"),
    ),
    # Over-ride Django admin default login/logout
    path("admin/login/", lambda r: redirect("/login/auth0", permanent=False)),
    path("admin/logout/", lambda r: redirect("/logout", permanent=False)),
    path("admin/", admin.site.urls),
]
