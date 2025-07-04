from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from products import views
from products import urls as products_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    #path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
