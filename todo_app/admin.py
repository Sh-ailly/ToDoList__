from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, todomodel

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('My Customization', {'fields':['whattodo']})
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'whattodo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'whattodo')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(todomodel)
