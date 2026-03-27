import base64
from datetime import datetime
import requests
from django.conf import settings


class MpesaService:
    def __init__(self):
        self.config = settings.MPESA_CONFIG

    def _base_url(self):
        return (
            'https://api.safaricom.co.ke'
            if self.config['environment'] == 'production'
            else 'https://sandbox.safaricom.co.ke'
        )

    def _get_access_token(self):
        base_url = self._base_url()
        response = requests.get(
            f'{base_url}/oauth/v1/generate?grant_type=client_credentials',
            auth=(self.config['consumer_key'], self.config['consumer_secret']),
            timeout=self.config['timeout_seconds'],
        )
        response.raise_for_status()
        return response.json()['access_token']

    def initiate_stk_push(self, order):
        if self.config['mock_mode']:
            return {
                'success': True,
                'merchant_request_id': f'mock-merchant-{order.id}',
                'checkout_request_id': f'mock-checkout-{order.id}',
                'response_description': 'Mock STK Push initiated',
            }

        access_token = self._get_access_token()
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.config['shortcode']}{self.config['passkey']}{timestamp}".encode()
        ).decode()

        payload = {
            'BusinessShortCode': self.config['shortcode'],
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(order.amount),
            'PartyA': order.customer_phone,
            'PartyB': self.config['shortcode'],
            'PhoneNumber': order.customer_phone,
            'CallBackURL': self.config['callback_url'],
            'AccountReference': str(order.id),
            'TransactionDesc': f'Purchase of {order.program.title}',
        }

        base_url = self._base_url()
        response = requests.post(
            f'{base_url}/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=self.config['timeout_seconds'],
        )
        response.raise_for_status()
        data = response.json()

        return {
            'success': data.get('ResponseCode') == '0',
            'merchant_request_id': data.get('MerchantRequestID', ''),
            'checkout_request_id': data.get('CheckoutRequestID', ''),
            'response_description': data.get('ResponseDescription', ''),
            'raw': data,
        }
