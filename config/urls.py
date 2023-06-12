from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("config.pokemons")),
    path("", include("core.create_user")),
]
