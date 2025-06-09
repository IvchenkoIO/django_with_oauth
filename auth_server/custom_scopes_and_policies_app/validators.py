# oauth_consent/validators.py
import json
from urllib.parse import parse_qs

from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import Application
from custom_scopes_and_policies_app.models import CustomGrant

print("✅ Loading CustomOAuth2Validator…")

class CustomOAuth2Validator(OAuth2Validator):
    def save_authorization_code(self, client_id, code, request, *args, **kwargs):

        super().save_authorization_code(client_id, code, request, *args, **kwargs)

        code_str = code.get("code")
        if not code_str:
            return

        # 1) Make sure DOT actually wrote a row into CustomGrant
        try:
            grant = CustomGrant.objects.get(code=code_str)
        except CustomGrant.DoesNotExist:
            print("✖ No CustomGrant found for code", code_str)
            return
        print("✔ Found CustomGrant for code", code_str)

        # 2a) gettint the json info from the request
        raw = getattr(request, 'authorization_details', None)
        if raw is None:
            print("✖ No authorization_details found for code", code_str," trying different option ....")
            raw = request.POST.get('authorization_details') or request.GET.get('authorization_details')

        if not raw:
            print("✖ No authorization_details present in GET or POST")
            return

        # 3) Parse & save it into the grant
        try:
            grant.policy_levels = json.loads(raw)
            grant.save(update_fields=["policy_levels"])
            print("✔ Saved policy_levels on CustomGrant:", grant.policy_levels)
        except json.JSONDecodeError:
            print("✖ Failed to JSON-decode authorization_details:", raw)
            return

    def save_bearer_token(self, token, request, *args, **kwargs):
        # 1) Build & persist the core token dict
        ret = super().save_bearer_token(token, request, *args, **kwargs)

        # 2) Extract the one-time code from the token-exchange body
        body = getattr(request, 'body', b'')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        code = parse_qs(body).get('code', [None])[0]

        # 3) If we have it, look up our grant & merge in the JSON
        if code:
            try:
                grant = CustomGrant.objects.get(code=code)
                if grant.policy_levels:
                    token['authorization_details'] = grant.policy_levels
                    print("✔ Succesfully loaded authorization_details into access token ...", grant.policy_levels)
            except CustomGrant.DoesNotExist:
                print("✖ Failed to load authorization_details into access token ...")
                pass

        return ret
