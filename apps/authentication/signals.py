from allauth.account.signals import email_confirmed
from django.dispatch import receiver

@receiver(email_confirmed)
def activate_user(sender, request, email_address, **kwargs):
    # Activate the user after email confirmation
    user = email_address.user
    if not user.is_active:
        user.is_active = True
        user.save()
        print(f"User {user.username} has been activated.")  # Debugging
    else:
        print(f"User {user.username} is already active.")
    # You can add additional logic here if needed
    # For example, you might want to log this event or send a notification
    # Send a notification to the user after activation
    user.email_user(
        subject="Account Activated",
        message="Your account has been successfully activated. You can now log in and start using the app.",
        from_email="noreply@chlosta.live"
    )
    