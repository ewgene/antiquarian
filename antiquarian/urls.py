from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from products import views
from products import urls as products_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]
