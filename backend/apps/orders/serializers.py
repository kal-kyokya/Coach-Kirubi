from rest_framework import serializers
from apps.programs.models import Program
from .models import Order


class CheckoutSerializer(serializers.Serializer):
    program_slug = serializers.SlugField()
    customer_name = serializers.CharField(max_length=120)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)

    def validate_program_slug(self, value):
        if not Program.objects.filter(slug=value, is_published=True).exists():
            raise serializers.ValidationError('Selected program does not exist.')
        return value


class OrderStatusSerializer(serializers.ModelSerializer):
    program_title = serializers.CharField(source='program.title', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'program_title',
            'amount',
            'status',
            'access_granted',
            'mpesa_receipt_number',
            'created_at',
        ]
