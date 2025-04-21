from django.contrib import admin
from .models import Delivery

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address', 'quantity', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'customer__email', 'address')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('customer',)}),
        ('Delivery Details', {'fields': ('address', 'quantity', 'status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('customer',)

# Register models with custom admin classes
admin.site.register(Delivery, DeliveryAdmin)