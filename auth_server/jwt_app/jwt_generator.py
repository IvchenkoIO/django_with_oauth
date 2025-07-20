
'''
jwt_app/jwt_generator.py
-----------------------

Custom JWT generator for OAuth2 access tokens using RS256.

Responsibilities:
  - Extract authentication and authorization context from the request.
  - Build standard JWT claims (sub, iat, exp, jti, scope).
  - Include custom authorization_details (policy levels) if available.
  - Sign the payload with the private RSA key from settings.
  - Return the encoded JWT string.
'''

import uuid
from urllib.parse import parse_qs

import jwt
import datetime
from django.conf import settings
import time
import logging


# Initialize logger for this module
logger = logging.getLogger(__name__)


def _get_authorization_details(request):
    """
    Retrieve custom authorization details from the request or fallback to CustomGrant lookup.

    Args:
        request (HttpRequest): Django request, may have .authorization_details or .body containing code.

    Returns:
        Optional[dict]: Policy levels or authorization details, or None if unavailable.
    """
    # Use details directly attached to the request if present
    auth_details = getattr(request, 'authorization_details', None)
    if auth_details:
        return auth_details

    # Fallback: parse authorization code from request body
    raw_body = getattr(request, 'body', b'')
    if isinstance(raw_body, (bytes, bytearray)):
        raw_body = raw_body.decode('utf-8', errors='ignore')

    code = parse_qs(raw_body).get('code', [None])[0]
    if not code:
        return None

    try:
        from custom_scopes_and_policies_app.models import CustomGrant
        grant = CustomGrant.objects.get(code=code)
        return grant.policy_levels
    except ImportError as e:
        logger.error("Failed to import CustomGrant model: %s", e)
    except CustomGrant.DoesNotExist:
        logger.info("No CustomGrant found for code %s", code)
    except Exception as e:
        logger.warning("Unexpected error retrieving CustomGrant for code %s: %s", code, e)
    return None

def generate_jwt(request, *args, **kwargs):
    """
    Generate an RS256-signed JWT for the current authenticated request.

    Args:
        request (HttpRequest): Django request, expected to have .user and body/authorization details.
        *args, **kwargs: Additional parameters passed by django-oauth-toolkit (ignored).

    Returns:
        str: Encoded JWT containing user and authorization information.

    JWT Claims:
        sub (str): Subject, the user primary key or None.
        iat (int): Issued-at time (Unix timestamp).
        exp (int): Expiration time (Unix timestamp = now + ACCESS_TOKEN_EXPIRE_SECONDS).
        jti (str): Unique JWT ID (UUID4).
        scope (str): Requested OAuth2 scopes.
        authorization_details (optional): Custom grant policy levels or details.
    """


    # Attempt to retrieve information from the request.
    from custom_scopes_and_policies_app.models import CustomGrant
    from oauth2_provider.models import Application
    
    # Load token lifetime (seconds) from settings, default to 36000 (10h)
    exp_seconds = settings.OAUTH2_PROVIDER.get('ACCESS_TOKEN_EXPIRE_SECONDS', 36000)
    
    # Current time as Unix timestamp
    now = int(time.time())
    exp=now + exp_seconds
    
    # DOT doesn’t pass token & user here, so we only have 'request'.
    # If you ever need scope/client you can parse those similarly from the request.
    # Base payload with standard claims
    payload = {
        "sub": str(request.user.pk) if request.user else None,
        #"aud": settings.JWT_AUDIENCE,  # e.g. "https://api.mydomain.com"
        "iat": now,
        "exp": now + exp_seconds,
        "jti": str(uuid.uuid4()),
        "scope": getattr(request, "scopes", getattr(request, "scope", "")),
    }

    
    # Attach custom authorization details if available
    details = _get_authorization_details(request)
    if details is not None:
        payload['authorization_details'] = details

    # Encode JWT with RS256 using the private key from settings
    token_str = jwt.encode(
        payload,
        settings.JWT_PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    # jwt.encode may return bytes in some versions
    if isinstance(token_str, bytes):
        token_str = token_str.decode('utf-8')
    return token_str