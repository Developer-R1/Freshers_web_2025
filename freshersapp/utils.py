import random
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings



def send_otp(email):
    otp = str(random.randint(100000, 999999))  # 6-digit OTP
    subject = "Your OTP Verification Code"
    message = f"Your OTP is {otp}. Please enter this to complete your registration."
    
    send_mail(subject, message, None, [email])  # None uses DEFAULT_FROM_EMAIL
    
    return otp

# keep track of which account to use next in round robin
# current_index = 0

# def generate_otp():
    
#     return str(random.randint(100000, 999999))

# def send_otp(email):
  
#     global current_index

#     otp = generate_otp()
#     subject = "Your OTP Verification Code for Freshers 2K25 Website"
#     message = f"Your OTP is: {otp}. Please enter this to complete your registration."

    
#     accounts = settings.EMAIL_ACCOUNTS
#     if not accounts:
#         raise ValueError("EMAIL_ACCOUNTS is not configured in settings.py")

    
#     account = accounts[current_index]

    
#     connection = get_connection(
#         host=account["EMAIL_HOST"],
#         port=account["EMAIL_PORT"],
#         username=account["EMAIL_HOST_USER"],
#         password=account["EMAIL_HOST_PASSWORD"],
#         use_tls=True
#     )


#     from_email = account["EMAIL_HOST_USER"]
#     email_obj = EmailMessage(subject, message, from_email, [email], connection=connection)
#     email_obj.send()

   
#     current_index = (current_index + 1) % len(accounts)

#     return otp