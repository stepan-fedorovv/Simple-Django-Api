import jwt
from django.conf import settings


def generate_token(data):
    token = jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    data = {"access_token": token}
    return data
