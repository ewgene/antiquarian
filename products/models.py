from django.db import models # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from django.urls import reverse # type: ignore
from django.utils.text import slugify # type: ignore
import re
#from django.contrib.auth import get_user_model # type: ignore

#User = get_user_model()


def create_slug(text):
    """Create a slug from text, handling Cyrillic characters"""
    if not text:
        return ''
    
    # Convert Cyrillic to Latin (basic mapping)
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    # Convert Cyrillic to Latin
    converted = ''
    for char in text:
        converted += cyrillic_to_latin.get(char, char)
    
    # Use Django's slugify on the converted text
    slug = slugify(converted)
    
    # If still empty, create a fallback slug
    if not slug:
        # Remove special characters and convert to lowercase
        slug = re.sub(r'[^\w\s-]', '', converted.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # If still empty, use a generic slug
        if not slug:
            slug = 'product'
    
    return slug


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
    slug = models.SlugField(max_length=300, unique=True, blank=True)
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
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = create_slug(self.name)
            slug = base_slug
            counter = 1
            
            # Check if slug already exists and generate a unique one
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_gallery")
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.alt_text or 'Image'}"
