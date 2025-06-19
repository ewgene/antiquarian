from django.shortcuts import render # type: ignore
from django.views.generic import ListView, DetailView # type: ignore
from products.models import Product # type: ignore
from rest_framework import viewsets # type: ignore
from .models import Product, ProductCategory, ProductImage # type: ignore
from .filters import ProductFilter
from .serializer import ProductSerializer, ProductCategorySerializer, ProductImageSerializer # type: ignore

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def list_products(self, request):
         return render(request, 'products/home.html')

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductImageSerializer(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class Home(ListView):
    model = Product
    template_name = 'products/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

def home(request):
    product_list = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, 'products/home.html', {'filter': product_filter})

class ProductDetail(DetailView):
	model = Product
	template_name = 'products/product_detail.html'