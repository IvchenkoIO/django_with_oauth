import jwt
import datetime
from django.conf import settings

def generate_jwt(request, token, user, *args, **kwargs):
    exp_seconds = settings.OAUTH2_PROVIDER.get('ACCESS_TOKEN_EXPIRE_SECONDS', 36000)
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)

    payload = {
        'user_id': user.pk,
        'exp': exp,
        'scope': token.scope,
        'token_type': token.token_type,
        'client_id': token.application.client_id,
    }

    token_str = jwt.encode(
        payload,
        settings.JWT_PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    if isinstance(token_str, bytes):
        token_str = token_str.decode('utf-8')

    return token_str