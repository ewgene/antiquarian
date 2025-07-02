from django.core.management.base import BaseCommand # type: ignore
from django.utils.text import slugify # type: ignore
from products.models import Product
import re


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


class Command(BaseCommand):
    help = 'Fix duplicate slugs by adding counter suffixes'

    def handle(self, *args, **options):
        self.stdout.write('Starting to fix duplicate slugs...')
        
        # Get all products and group them by their base slug
        products = Product.objects.all().order_by('id')
        slug_counts = {}
        fixed_count = 0
        
        for product in products:
            if not product.slug:
                # Generate slug if it doesn't exist
                base_slug = create_slug(product.name)
            else:
                # Extract base slug (remove any existing counter)
                base_slug = product.slug
                if '-' in base_slug:
                    # Check if the part after the last dash is a number
                    parts = base_slug.split('-')
                    if parts[-1].isdigit():
                        base_slug = '-'.join(parts[:-1])
            
            # Count occurrences of this base slug
            if base_slug not in slug_counts:
                slug_counts[base_slug] = 0
            slug_counts[base_slug] += 1
            
            # Generate unique slug
            if slug_counts[base_slug] == 1:
                new_slug = base_slug
            else:
                new_slug = f"{base_slug}-{slug_counts[base_slug] - 1}"
            
            # Update the product if slug changed
            if product.slug != new_slug:
                old_slug = product.slug
                product.slug = new_slug
                product.save(update_fields=['slug'])
                self.stdout.write(f'Fixed slug for "{product.name}": {old_slug} -> {new_slug}')
                fixed_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} duplicate slugs!')
        ) 