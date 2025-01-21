from django.core.mail import send_mail
from django.conf import settings

def sendEmailToClient():
    subject = "Demo Email"
    message = "This is a demo email by my Django server"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['chakrabortysarthak5@gmail.com']

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        # Handle the exception (e.g., log the error)
        print("An error occurred while sending the email:", e)
