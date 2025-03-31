import jwt
import datetime
from django.conf import settings

def generate_jwt(request, *args, **kwargs):
    # Attempt to retrieve information from the request.
    user = getattr(request, 'user', None)
    # DOT might attach the client as 'client' or 'application'
    client = getattr(request, 'client', getattr(request, 'application', None))
    # Similarly, scope might be attached as 'scopes' or 'scope'
    scope = getattr(request, 'scopes', getattr(request, 'scope', None))
    token_type = "Bearer"  # Set the token type; adjust if needed.

    exp_seconds = settings.OAUTH2_PROVIDER.get('ACCESS_TOKEN_EXPIRE_SECONDS', 36000)
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)

    payload = {
        'user_id': user.pk if user else None,
        'exp': exp,
        'scope': scope,
        'token_type': token_type,
        'client_id': client.client_id if client else None,
        # Add any additional claims here as needed.
    }

    token_str = jwt.encode(
        payload,
        settings.JWT_PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    if isinstance(token_str, bytes):
        token_str = token_str.decode('utf-8')
    return token_str