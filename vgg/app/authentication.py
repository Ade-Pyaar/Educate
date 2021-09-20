from django.conf import settings
import string, jwt
from random import choices
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication




def get_random_token(length):
    '''generates token'''
    return ''.join(choices(string.ascii_uppercase + string.digits, k=length))



# timedelta(minutes=x)    x is an int that determines token expiration time
def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=60), **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )


def get_refresh_token():
    return jwt.encode(
        {'exp': datetime.now() + timedelta(days=365), 'data': get_random_token(15)},
        settings.SECRET_KEY,
        algorithm='HS256'
    )









class MyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None

        return self.get_user(data['user_id']), None

        
        
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception:
            return None



    def validate_request(self, headers):
        authorization = headers.get('Authorization', None)
        if not authorization:
            return None
        token = headers['Authorization'][7:]
        decoded_data = self.verify_token(token)
        if not decoded_data:
            return None
        return decoded_data


    @staticmethod
    def verify_token(token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except Exception:
            return None

        exp = decoded['exp']

        if datetime.now().timestamp() > exp:
            return None
        
        return decoded