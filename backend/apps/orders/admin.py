from django.contrib import admin
from .models import Order, PaymentEvent


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'program',
        'customer_email',
        'amount',
        'status',
        'access_granted',
        'created_at',
    )
    list_filter = ('status', 'access_granted', 'created_at')
    search_fields = ('customer_email', 'customer_name', 'mpesa_checkout_request_id', 'mpesa_receipt_number')
    readonly_fields = ('created_at', 'updated_at', 'mpesa_checkout_request_id', 'mpesa_receipt_number')

@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ('order', 'event_type', 'success', 'created_at')
    list_filter = ('event_type', 'success', 'created_at')
    search_fields = ('customer_email', 'customer_name', 'mpesa_checkout_request_id', 'mpesa_receipt_number')
    readonly_fields = ('created_at',)
