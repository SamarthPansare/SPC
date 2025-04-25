from django.contrib import admin
from .models import CustomUser, Role, UsersStudent, UsersTeacher, UsersNonTeachingStaff

# Register your models here.

admin.site.register(UsersStudent)
admin.site.register(UsersTeacher)
admin.site.register(UsersNonTeachingStaff)
admin.site.register(Role)

# Customize the admin interface for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']  # Display these fields in the admin list view
    list_filter = ['user_type']  # Add filter by user_type
    search_fields = ['username', 'email']  # Add search functionality for username and email

admin.site.register(CustomUser, CustomUserAdmin)