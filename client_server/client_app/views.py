from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings as settings
import urllib.parse
import base64
import hashlib
import requests
import os
import json


def generate_pkce():
    """
    Generates a code verifier and code challenge for PKCE.
    """
    # Generate a random URL-safe string as the code verifier.
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')
    # Compute the code challenge using SHA-256 hash.
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge



def oauth_callback(request):

    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No authorization code provided'}, status=400)
    code_verifier = request.session.get('pkce_verifier')
    print("code_verifier CALLBACK", code_verifier)
    token_url = f"{settings.NGROK_URL}/auth/o/token/"  # Adjust to your auth server URL
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': f"{settings.NGROK_URL}/client/oauth/callback/",
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        # If using PKCE, include 'code_verifier'
        ##'code_verifier': code_verifier,
    }
    response = requests.post(token_url, data=payload , verify=False)
    token_data = response.json()
    if 'access_token' not in token_data:
        return JsonResponse({'error': 'Failed to obtain token', 'details': token_data}, status=400)

    # Save the access token in session or secure storage
    try:
        token_data = response.json()
    except Exception as e:
        return JsonResponse({'error': 'Failed to decode token response', 'details': str(e)}, status=400)

    print("Token data received from auth server:", token_data)  # Debug output

    if 'access_token' not in token_data:
        return JsonResponse({'error': 'Failed to obtain token', 'details': token_data}, status=400)

    request.session['access_token'] = token_data['access_token']
    return HttpResponseRedirect('/client/client/')

def client_home(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token. Please authenticate.'}, status=401)

    headers = {'Authorization': f'Bearer {access_token}'}
    resource_response = requests.get(f"{settings.NGROK_URL}/resource/api/photos/", headers=headers)
    try:
        data = resource_response.json()
    except Exception:
        data = {'error': 'Invalid response from resource server'}
    
    data_json = json.dumps(data)
    print(data_json)
    return render(request, 'app.html', {
        'data_json': data_json
    })

    ##return JsonResponse(data)


def oauth_login(request):
    ##code_verifier, code_challenge = generate_pkce()
    # Save the verifier in the session for later use.
    ##request.session['pkce_verifier'] = code_verifier
    ##request.session.modified = True
    ##request.session.save()
    print(settings.NGROK_URL)
    print("Session key after storing code_verifier:", request.session.session_key)
    #print("code_verifier", code_verifier)
    # The auth server's authorization endpoint
    auth_url = f"{settings.NGROK_URL}/auth/auth"

    # Prepare the query parameters (make sure these match your client registration)
    params = {
        'response_type': 'code',
        'client_id': settings.OAUTH_CLIENT_ID,  # Your registered client ID
        'redirect_uri': f"{settings.NGROK_URL}/client/oauth/callback/",
        'scope': 'read',  # Or another scope you have defined
        #'code_challenge': code_challenge,
        #'code_challenge_method': 'S256',
    }

    # Construct the full URL
    full_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    return HttpResponseRedirect(full_url)


def debug_session(request):
    request.session['test'] = 'hello'
    return JsonResponse({'session': dict(request.session.items())})