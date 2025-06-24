from django.contrib import admin
from django.urls import include, path
from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("question/", include("question.urls")),
    path("statistics/", include("stats.urls")),
    path("", index, name="index"),
]
