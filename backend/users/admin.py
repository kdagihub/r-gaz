from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VendorProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'is_verified_email', 'is_approved_vendor', 'is_staff', 'is_active')
    list_filter = ('role', 'is_verified_email', 'is_approved_vendor', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Location', {'fields': ('address', 'location')}),
        ('Role & Status', {'fields': ('role', 'is_verified_email', 'is_approved_vendor')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'status', 'average_rating')
    list_filter = ('status',)
    search_fields = ('business_name', 'user__username', 'user__email', 'address')
    ordering = ('business_name',)
    
    fieldsets = (
        (None, {'fields': ('user', 'business_name')}),
        ('Location', {'fields': ('address', 'location')}),
        ('Status', {'fields': ('status', 'average_rating')}),
    )
    
    raw_id_fields = ('user',)

# Register models with custom admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(VendorProfile, VendorProfileAdmin)