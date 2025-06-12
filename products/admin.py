from django.contrib import admin # type: ignore

from products.models import Product, ProductCategory, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)