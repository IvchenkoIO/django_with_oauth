
'''
custom_scopes_and_policies_app/views.py
---------------------------------------

Views for rendering and processing custom OAuth2 scope and policy selection by the end-user.

Classes:
  - ScopeSelectionView: Handles GET to display available scopes and policies,
    POST to collect user's choices and redirect to the OAuth2 authorize endpoint.
'''

from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import urllib
import json
import logging

# Initialize module logger
logger = logging.getLogger(__name__)

class ScopeSelectionView(View):
    """
    Display a form for users to select OAuth2 scopes and custom policy levels,
    and handle form submission by redirecting back to the OAuth2 authorize URL
    with selected parameters.
    """

    template_name = "custom_scopes_and_policy.html"

    def get(self, request):
        """
        Render the scope and policy selection template.

        Context keys:
            - all_scopes (dict): Available scope keys and descriptions.
            - policy_types (dict): Mapping of data types to list of policy levels.
            - client_id (str): OAuth2 client ID from query params.
            - redirect_uri (str): Redirect URI from query params.
            - response_type (str): OAuth2 response_type (default 'code').
            - state (str): Opaque state parameter to maintain request integrity.
        """


        scopes  = settings.OAUTH2_PROVIDER['SCOPES']
        # grab the new policy-levels dict
        policies = settings.OAUTH2_PROVIDER.get('POLICY_LEVELS', {})
        ctx = {
            'all_scopes':   scopes,
            'policy_types': policies,  # dict: data_type → [levels]
            'client_id':    request.GET.get('client_id'),
            'redirect_uri': request.GET.get('redirect_uri'),
            'response_type':request.GET.get('response_type', 'code'),
            'state':         request.GET.get('state', ''),
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        """
        Process user selections and redirect to the OAuth2 authorization endpoint.

        Steps:
            1. Read selected scopes from POST data.
            2. Collect policy levels for each data type.
            3. Serialize policy_levels to JSON under 'authorization_details'.
            4. Build query params including client_id, redirect_uri, response_type,
               scope string, authorization_details, and state.
            5. Redirect user to /oauth2/authorize/?<params>.
        """
        # 1) Extract selected scopes
        chosen_scopes = request.POST.getlist('scopes')

        # 2) Build custom policy levels dict
        policy_levels = {}
        for data_type in settings.OAUTH2_PROVIDER.get('POLICY_LEVELS', {}):
            # default if nothing selected?
            level = request.POST.get(f"policy_{data_type}")
            if level:
                policy_levels[data_type] = level

        # 3) Serialize policy details
        auth_details = json.dumps(policy_levels)

        # 4) Construct redirect parameters
        params = {
            'client_id':    request.POST['client_id'],
            'redirect_uri': request.POST['redirect_uri'],
            'response_type':request.POST['response_type'],
            'scope': " ".join(chosen_scopes),
            #'scope':        " ".join(chosen_scopes),
            # include your policy info under a custom param—
            # e.g. if you’ll read it from request.body in your validator
            'authorization_details': auth_details,
            'state':        request.POST.get('state', ''),
        }
        # Debug log for tracing redirect URL construction
        logger.debug("Redirecting to OAuth authorize with params: %s", params)
        # 5) Perform the redirect
        authorize_url = reverse('oauth2_provider:authorize')
        redirect_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"
        return redirect(redirect_url)

