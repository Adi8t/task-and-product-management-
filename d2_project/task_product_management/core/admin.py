from django.contrib import admin
from .models import Category, Product ,Task

# Category Admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category')  

# Product Admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category', 'is_active')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id',"title","description","due_date","status","product","assigned_user")

# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Task ,TaskAdmin)