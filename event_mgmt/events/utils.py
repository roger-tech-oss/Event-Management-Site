import razorpay
from django.conf import settings

def get_razorpay_client():
    """
    Returns a Razorpay client object using credentials from Django settings.
    """
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
