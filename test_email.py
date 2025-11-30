import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petpalproject.settings')
django.setup()

from django.core.mail import send_mail

print("Testing email configuration...")
print("="*60)

try:
    send_mail(
        'Test Email - Password Reset',
        'This is a test email. If you see this in your terminal, the email system is working!',
        'noreply@petpal.com',
        ['test@example.com'],
        fail_silently=False,
    )
    print("\n✓ Email sent successfully!")
    print("Check the output above - the email should be printed there.")
except Exception as e:
    print(f"\n✗ Error sending email: {e}")
