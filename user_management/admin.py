from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')

    # Specify the fields that should not be editable
    readonly_fields = ['last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password','role')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthdate', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ['last_login']}),  # Marked as read-only
    )

# Register the CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
