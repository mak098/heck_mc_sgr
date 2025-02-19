from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        ('identifier', {
            'fields': ('username', 'password'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        })
    )
    
    filter_horizontal =('groups',)


