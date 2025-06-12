from django.db import models # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
#from django.contrib.auth import get_user_model # type: ignore

#User = get_user_model()


class ProductCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=120)
    icon = models.ImageField(upload_to="category_icons", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        
    def __str__(self):
        return self.name
    

def get_default_product_category():
    return ProductCategory.objects.get_or_create(name="Others")[0]

CONDITION_CHOICES = [
    ('new', 'Отличное'),
    ('used', 'Хорошее'),
    ('refurbished', 'С реставрацией'),
    ('broken', 'Требует реставрации'),
    ('other', 'Другое'),
]

class Product(models.Model):
    mainimage = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Краткое описание', blank=True)
    detail_text = models.TextField(max_length=1000, verbose_name='Подробнее', blank=True)
    material = models.TextField(max_length=500, blank=True, verbose_name='Материал', default='')
    production_date = models.TextField(max_length=200, blank=True, verbose_name='Годы выпуска', default='')
    price = models.FloatField(default=0)
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Состояние", default='used')    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_gallery")
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.alt_text or 'Image'}"
