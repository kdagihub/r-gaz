from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('user', 'amount', 'status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)

admin.site.register(Payment, PaymentAdmin)