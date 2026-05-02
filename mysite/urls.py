from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from mysite.sitemaps import HomeSitemap, CategorySitemap, ProductSitemap, PostSitemap


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {getattr(settings, 'SITE_URL', '')}/sitemap.xml",
        "",
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /summernote/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


sitemaps = {
    "home": HomeSitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
    "posts": PostSitemap,
}


urlpatterns = [
    path('', include('blog.urls')),
    path('products/', include('products.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('robots.txt', robots_txt, name="robots"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]