import os
import urllib.request
from django.core.files.base import ContentFile
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
django.setup()

from products.models import Product, Category
from blog.models import Post

def download_image(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read()

# Default fallback images
FALLBACK_FOOD = "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800&q=80"
FALLBACK_WET = "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=800&q=80"
FALLBACK_LITTER = "https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?w=800&q=80"

for p in Product.objects.all():
    if p.image and not os.path.exists(os.path.join(settings.MEDIA_ROOT, p.image.name)):
        print(f"Recovering image for product: {p.slug}")
        img_url = FALLBACK_WET if 'wet' in p.slug else FALLBACK_FOOD
        img_data = download_image(img_url)
        p.image.save(os.path.basename(p.image.name), ContentFile(img_data), save=True)

for c in Category.objects.all():
    if c.image and not os.path.exists(os.path.join(settings.MEDIA_ROOT, c.image.name)):
        print(f"Recovering image for category: {c.slug}")
        img_url = FALLBACK_WET if 'wet' in c.slug else FALLBACK_FOOD
        img_data = download_image(img_url)
        c.image.save(os.path.basename(c.image.name), ContentFile(img_data), save=True)

for post in Post.objects.all():
    if post.featured_image and not os.path.exists(os.path.join(settings.MEDIA_ROOT, post.featured_image.name)):
        print(f"Recovering image for post: {post.slug}")
        img_url = FALLBACK_LITTER if 'litter' in post.slug else FALLBACK_FOOD
        img_data = download_image(img_url)
        post.featured_image.save(os.path.basename(post.featured_image.name), ContentFile(img_data), save=True)

print("Recovery finished.")
