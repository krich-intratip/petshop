from django.contrib import admin
from .models import Category, Product, FAQ
from django_summernote.admin import SummernoteModelAdmin


# Add TabularInline for FAQ
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1  # Number of empty FAQ forms to display


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FAQInline] 


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('body')


# Register the FAQ model separately (optional)
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'created', 'updated']
    list_filter = ['category', 'created', 'updated']
    search_fields = ['question', 'answer']

