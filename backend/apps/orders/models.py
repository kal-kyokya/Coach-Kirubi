import uuid
from django.db import models
from apps.programs.models import Program


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'pending'),
        (STATUS_PAID, 'paid'),
        (STATUS_FAILED, 'failed'),
        (STATUS_CANCELLED, 'cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='orders')
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    mpesa_checkout_request_id = models.CharField(max_length=120, blank=True, unique=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=120, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    access_granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer_email} - {self.program.title} ({self.status})'


class PaymentEvent(models.Model):
    EVENT_INITIATE = 'initiate'
    EVENT_CALLBACK = 'callback'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20)
    payload = models.JSONField(default=dict)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
