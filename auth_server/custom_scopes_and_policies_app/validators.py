# oauth_consent/validators.py
'''
custom_scopes_and_policies_app/validators.py
-------------------------------------------

Custom OAuth2 validator extending django-oauth-toolkit to persist and
propagate custom policy-level details alongside authorization codes and tokens.

Classes:
    - CustomOAuth2Validator: Overrides DOT methods to attach 'authorization_details'
      (policy_levels) to CustomGrant and to the issued access token.
'''




import json
from urllib.parse import parse_qs

from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import Application
from custom_scopes_and_policies_app.models import CustomGrant
import logging

# Module logger
logger = logging.getLogger(__name__)

print("✅ Loading CustomOAuth2Validator…")

class CustomOAuth2Validator(OAuth2Validator):
    
    """
    Extends the default OAuth2Validator to handle custom policy-level data.

    This validator intercepts two key processes:
      1. save_authorization_code: Saves incoming 'authorization_details' JSON
         into the corresponding CustomGrant.policy_levels field.
      2. save_bearer_token: Transfers stored policy_levels from CustomGrant
         into the JWT payload (token dict) under 'authorization_details'.
    """


    def save_authorization_code(self, client_id, code, request, *args, **kwargs):


        """
        Called when an authorization code is created.

        1. Delegates to superclass to persist base code data.
        2. Retrieves the raw code string and corresponding CustomGrant.
        3. Extracts 'authorization_details' JSON from request attributes or POST/GET.
        4. Parses and stores policy_levels on the CustomGrant instance.

        Args:
            client_id (str): OAuth2 client identifier.
            code (dict): Dict with at least 'code' key.
            request (HttpRequest): HTTP request carrying optional JSON payload.
        """

        # 1) Persist default authorization code data
        super().save_authorization_code(client_id, code, request, *args, **kwargs)

        # 2) Extract code string
        code_str = code.get("code")
        if not code_str:
            logger.warning("save_authorization_code: missing code value")
            return

        # 3) Lookup associated CustomGrant
        try:
            grant = CustomGrant.objects.get(code=code_str)
            logger.debug("✔ Found CustomGrant for code %s", code_str)
        except CustomGrant.DoesNotExist:
            logger.error("No CustomGrant found for code %s", code_str)
            return
        

        # 4) Extract authorization_details JSON
        raw = getattr(request, 'authorization_details', None)
        if raw is None:
            logger.debug(
                "No request.authorization_details; checking POST/GET for code %s", code_str
            )
            raw = request.POST.get('authorization_details') or request.GET.get('authorization_details')

        if not raw:
            logger.error(
                "No authorization_details provided for code %s", code_str
            )
            return

         # 5) Parse and save policy_levels
        try:
            grant.policy_levels = json.loads(raw)
            grant.save(update_fields=["policy_levels"])
            logger.info(
                "Saved policy_levels on CustomGrant %s: %s",
                code_str,
                grant.policy_levels
            )
        except json.JSONDecodeError:
            logger.error(
                "Invalid JSON in authorization_details for code %s: %s",
                code_str,
                raw
            )
            return

    def save_bearer_token(self, token, request, *args, **kwargs):
        
        """
        Called when a bearer token is issued (token endpoint).

        1. Delegates to superclass to build the base token dict.
        2. Parses the original authorization code from request body.
        3. Retrieves the associated CustomGrant and injects policy_levels
           into the token under 'authorization_details'.

        Args:
            token (dict): Outgoing token payload dict.
            request (HttpRequest): HTTP request carrying original code.
        Returns:
            dict: Possibly modified token dict.
        """

        # 1) Build base token
        token_val = super().save_bearer_token(token, request, *args, **kwargs)

        # 2) Extract code from request body
        body = getattr(request, 'body', b'')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        code = parse_qs(body).get('code', [None])[0]

         # 3) Inject policy_levels if available
        if code:
            try:
                grant = CustomGrant.objects.get(code=code)
                if grant.policy_levels:
                    token['authorization_details'] = grant.policy_levels
                    logger.info(
                        "Loaded authorization_details into token for code %s: %s",
                        code,
                        grant.policy_levels
                    )
            except CustomGrant.DoesNotExist:
                logger.warning(
                    "No CustomGrant for code %s; skipping authorization_details injection",
                    code
                )
            except Exception as e:
                logger.error(
                    "Error injecting authorization_details for code %s: %s",
                    code,
                    e
                )


        return token_val
