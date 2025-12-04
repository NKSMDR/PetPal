import hashlib
import hmac
import uuid
from django.conf import settings

class EsewaPayment:
    def __init__(self, product_code, success_url, failure_url, secret_key, amount, 
                 tax_amount='0', product_service_charge='0', product_delivery_charge='0', 
                 total_amount=None, transaction_uuid=None):
        self.product_code = product_code
        self.success_url = success_url
        self.failure_url = failure_url
        self.secret_key = secret_key
        self.amount = amount
        self.tax_amount = tax_amount
        self.product_service_charge = product_service_charge
        self.product_delivery_charge = product_delivery_charge
        self.total_amount = total_amount or amount
        self.transaction_uuid = transaction_uuid or str(uuid.uuid4())
        self.signature = None

    def create_signature(self):
        """Create signature for eSewa payment using HMAC-SHA256"""
        # Format: total_amount,transaction_uuid,product_code
        data_string = f"total_amount={self.total_amount},transaction_uuid={self.transaction_uuid},product_code={self.product_code}"
        
        # Create HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        self.signature = signature
        return self.signature

    def generate_form(self):
        """Generate HTML form for eSewa payment"""
        form_data = {
            'product_code': self.product_code,
            'success_url': self.success_url,
            'failure_url': self.failure_url,
            'amount': self.amount,
            'tax_amount': self.tax_amount,
            'product_service_charge': self.product_service_charge,
            'product_delivery_charge': self.product_delivery_charge,
            'total_amount': self.total_amount,
            'transaction_uuid': self.transaction_uuid,
            'signature': self.signature
        }
        
        # Generate HTML hidden input fields
        html_fields = ''
        for key, value in form_data.items():
            html_fields += f'<input type="hidden" name="{key}" value="{value}" />\n'
        
        return html_fields

    def is_completed(self, verify_signature=True):
        """Verify if payment is completed (simplified for testing)"""
        # In production, you would verify the signature and check with eSewa API
        # For now, we'll return True for testing purposes
        return True

    def verify_payment(self, response_data):
        """Verify payment response from eSewa"""
        # This would contain the actual verification logic
        # For now, we'll assume success if we get here
        return True
