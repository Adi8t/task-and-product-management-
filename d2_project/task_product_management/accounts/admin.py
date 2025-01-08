from django.contrib import admin

# Register your models here.


from .models import *
@admin.register(CustomUser)
class useradmin(admin.ModelAdmin):
    list_display= ['id']