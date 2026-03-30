from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/programs/', include('apps.programs.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/pages/', include('apps.pages.urls')),
]
