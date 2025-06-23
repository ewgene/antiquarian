from django.urls import include, path # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore

from products.views import ProductCategoryViewSet, ProductViewSet, home, Home, ProductDetail

app_name = "products"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r"products", ProductViewSet)


urlpatterns = [
    # Home page - accessible at root URL
    path("", home, name="home"),
    path("home/", home, name="home_alt"),
    path("home-class/", Home.as_view(), name="home_class"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    # Custom route for list_products action
    path("list-products/", ProductViewSet.as_view({'get': 'list_products'}), name="list_products"),
    # API routes
    path("api/", include(router.urls)),
]