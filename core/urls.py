from django.contrib import admin
from django.urls import path, include

from core.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('account.urls')),
    path('api/docs/', schema_view.with_ui()),
]
