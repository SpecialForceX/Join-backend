from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('board_app.urls')),
    path("api/auth/", include("auth_user_app.api.urls")),
]

