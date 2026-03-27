from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.programs.models import Program
from .models import Order, PaymentEvent
from .serializers import CheckoutSerializer, OrderStatusSerializer
from .services import MpesaService


class CheckoutAPIView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        program = Program.objects.get(slug=serializer.validated_data['program_slug'])
        with transaction.atomic():
            order = Order.objects.create(
                program=program,
                customer_name=serializer.validated_data['customer_name'],
                customer_email=serializer.validated_data['customer_email'],
                customer_phone=serializer.validated_data['customer_phone'],
                amount=program.price,
            )
            service = MpesaService()
            try:
                mpesa_response = service.initiate_stk_push(order)
            except Exception as exc:
                PaymentEvent.objects.create(
                    order=order,
                    event_type=PaymentEvent.EVENT_INITIATE,
                    payload={'error': str(exc)},
                    success=False,
                )
                order.status = Order.STATUS_FAILED
                order.save(update_fields=['status', 'updated_at'])
                return Response(
                    {'detail': 'Failed to start payment request. Please try again.'},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            order.mpesa_checkout_request_id = mpesa_response['checkout_request_id']
            order.save(update_fields=['mpesa_checkout_request_id', 'updated_at'])
            PaymentEvent.objects.create(
                order=order,
                event_type=PaymentEvent.EVENT_INITIATE,
                payload=mpesa_response,
                success=mpesa_response['success'],
            )

        return Response(
            {
                'order_id': str(order.id),
                'checkout_request_id': order.mpesa_checkout_request_id,
                'message': mpesa_response['response_description'],
            },
            status=status.HTTP_201_CREATED,
        )


class MpesaCallbackAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        callback = request.data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = callback.get('CheckoutRequestID')
        result_code = callback.get('ResultCode')

        if not checkout_request_id:
            return Response({'detail': 'Missing CheckoutRequestID'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.object.filter(mpesa_checkout_request_id=checkout_request_id).first()
        if not order:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        PaymentEvent.objects.create(
            order=order,
            event_type=PaymentEvent.EVENT_CALLBACK,
            payload=request.data,
            success=result_code == 0,
        )

        if order.status == Order.STATUS_PAID:
            return Response({'detail': 'Already processed'}, status=status.HTTP_200_OK)

        if result_code == 0:
            metadata_items = callback.get('CallbackMetadata', {}).get('Item', [])
            metadata = {item.get('Name'): item.get('Value') for item in metadata_items if 'Name' in item}
            order.status = Order.STATUS_PAID
            order.access_granted = True
            order.mpesa_receipt_number = str(metadata.get('MpesaReceiptNumber', ''))
            order.transaction_date = timezone.now()
            order.save(
                update_fields=['status', 'access_granted', 'mpesa_receipt_number', 'mpesa_receipt_number', 'transaction_data', 'update_at']
            )
        else:
            order.status = Order.STATUS_FAILED
            order.save(updated_fields=['status', 'updated_at'])

        return Response({'detail': 'Callback received'}, status=status.HTTP_200_OK)


class OrderStatusAPIView(APIView):
    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderStatusSerializer(order)
        return Response(serializer.data)
