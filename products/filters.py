from . models import Product
import django_filters # type: ignore
from django_filters.filters import RangeFilter # type: ignore


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = RangeFilter()


    class Meta:
        model = Product
        fields = ['name', 'price']