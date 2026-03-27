from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from apps.programs.models import Program
from .models import Order


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.program = Program.objects.create(
            title='Speed Foundations',
            short_description='Build explosive speed mechanics.',
            description='8-week sprint progression',
            price='2500.00',
            duration_weeks=8,
            level='beginner',
            delivery_format='hybrid',
            is_published=True,
        )

    @patch('apps.orders.services.MpesaService.initiate_stk_push')
    def test_checkout_creates_pending_order(self, mocked_stk):
        mocked_stk.return_value = {
            'success': True,
            'merchant_request_id': '123',
            'checkout_request_id': 'abc-123',
            'response_description': 'Sent',
        }
        response = self.client.post(
            '/api/orders/checkout/',
            {
                'program_slug': self.program.slug,
                'customer_name': 'Jane Doe',
                'customer_email': 'jane@example.com',
                'customer_phone': '254700111222',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(id=response.data['order_id'])
        self.assertEqual(order.status, Order.STATUS_PENDING)

    def test_callback_is_idempotent_for_paid_orders(self):
        order = Order.objects.create(
            program=self.program,
            customer_name='Jane Doe',
            customer_email='jane@example.com',
            customer_phone='254700111222',
            amount='2500.00',
            status=Order.STATUS_PAID,
            mpesa_checkout_request_id='abc-paid',
            access_granted=True,
        )
        payload = {
            'Body': {
                'stkCallback': {
                    'CheckoutRequestID': 'abc-paid',
                    'ResultCode': 0,
                    'CallbackMetadata': {'Item': []},
                }
            }
        }
        response = self.client.post('/api/orders/payments/mpesa/callback/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.STATUS_PAID)
