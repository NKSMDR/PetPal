import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petpalproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

print("="*80)
print("TESTING PASSWORD RESET FLOW")
print("="*80)

# Check if we have any users
users = User.objects.all()
print(f"\nTotal users in database: {users.count()}")

if users.exists():
    user = users.first()
    print(f"Testing with user: {user.username} ({user.email})")
    
    # Generate token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build reset link
    reset_link = f"http://127.0.0.1:8000/password-reset/confirm/{uid}/{token}/"
    
    print(f"\nGenerated reset link:")
    print(f"{reset_link}")
    
    # Send email
    subject = 'Password Reset Request - PetPal'
    message = f"""Hi {user.username},

You requested a password reset for your PetPal account.

Click the link below to reset your password:
{reset_link}

This link will expire in 24 hours.

If you didn't request this, please ignore this email.

Best regards,
The PetPal Team
"""
    
    print("\n" + "="*80)
    print("SENDING EMAIL (will appear below):")
    print("="*80 + "\n")
    
    send_mail(
        subject,
        message,
        'noreply@petpal.com',
        [user.email],
        fail_silently=False,
    )
    
    print("\n" + "="*80)
    print("✓ EMAIL SENT! The email content above shows what would be sent.")
    print(f"✓ Copy this link and paste it in your browser:")
    print(f"  {reset_link}")
    print("="*80)
else:
    print("\n✗ No users found in database!")
    print("  Please create a user first using the admin panel or register page.")
