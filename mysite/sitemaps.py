from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from products.models import Category, Product


class HomeSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return None


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Product.objects.filter(available=True)

    def lastmod(self, obj):
        return obj.updated


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date_updated
