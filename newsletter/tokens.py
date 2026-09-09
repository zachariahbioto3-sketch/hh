import hashlib, hmac
from django.conf import settings

def make_token(email):
    return hmac.new(settings.SECRET_KEY.encode(), email.encode(), hashlib.sha256).hexdigest()[:32]

def check_token(email, token):
    return hmac.compare_digest(make_token(email), token)
