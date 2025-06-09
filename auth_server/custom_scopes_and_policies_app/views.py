from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import urllib

# auth_app/views.py

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import urllib

class ScopeSelectionView(View):
    template_name = "custom_scopes_and_policy.html"

    def get(self, request):
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
        # scopes as before
        chosen_scopes = request.POST.getlist('scopes')

        # now grab each policy selection by its form-name
        # e.g. names "policy_numerical", "policy_images", ...
        policy_levels = {}
        for data_type in settings.OAUTH2_PROVIDER.get('POLICY_LEVELS', {}):
            # default if nothing selected?
            level = request.POST.get(f"policy_{data_type}")
            if level:
                policy_levels[data_type] = level

        # pack policy_levels into a JSON string (or however you consume it downstream)
        import json
        auth_details = json.dumps(policy_levels)
        cts={
            'lol':'lul',
            'lll':'aaa'
        }
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

        url = reverse('oauth2_provider:authorize')
        return redirect(f"{url}?{urllib.parse.urlencode(params)}")

