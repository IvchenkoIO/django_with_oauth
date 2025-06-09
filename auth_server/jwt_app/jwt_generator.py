import uuid
from urllib.parse import parse_qs

import jwt
import datetime
from django.conf import settings
import time
#from custom_scopes_and_policies_app.models import CustomGrant
#from oauth2_provider.models import Application

def generate_jwt(request, *args, **kwargs):
    # Attempt to retrieve information from the request.
    from custom_scopes_and_policies_app.models import CustomGrant
    from oauth2_provider.models import Application
    exp_seconds = settings.OAUTH2_PROVIDER.get('ACCESS_TOKEN_EXPIRE_SECONDS', 36000)
    now = int(time.time())
    exp=now + exp_seconds
    # DOT doesn’t pass token & user here, so we only have 'request'.
    # If you ever need scope/client you can parse those similarly from the request.
    payload = {
        "sub": str(request.user.pk) if request.user else None,
        #"aud": settings.JWT_AUDIENCE,  # e.g. "https://api.mydomain.com"
        "iat": now,
        "exp": now + exp_seconds,
        "jti": str(uuid.uuid4()),
        "scope": getattr(request, "scopes", getattr(request, "scope", "")),
    }

    auth_details = getattr(request, "authorization_details", None)

    if auth_details is not None:
        # If DOT parsed it for us, it’s already a dict. Just assign:
        payload["authorization_details"] = auth_details
    else:
        # Fallback: parse the 'code' from the /o/token/ POST body, then query CustomGrant.
        raw_body = getattr(request, "body", b"")
        if isinstance(raw_body, bytes):
            raw_body = raw_body.decode("utf-8")
        code = parse_qs(raw_body).get("code", [None])[0]

        if code:
            try:
                grant = CustomGrant.objects.get(code=code)
                if grant.policy_levels is not None:
                    payload["authorization_details"] = grant.policy_levels
            except CustomGrant.DoesNotExist:
                # No matching grant: nothing to add
                pass


    token_str = jwt.encode(
        payload,
        settings.JWT_PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    if isinstance(token_str, bytes):
        token_str = token_str.decode('utf-8')
    return token_str