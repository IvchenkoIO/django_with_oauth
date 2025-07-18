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
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)



def oauth_callback(request):
    """
    Handle the OAuth 2.0 authorization code callback from the authorization server.
    
    This view:
    1. Validates the presence of the authorization code
    2. Exchanges the authorization code for an access token
    3. Stores the access token in the session
    4. Redirects to the client login page on success
    
    
    Args:
        request (HttpRequest): The incoming request object containing:
            - GET parameter 'code': The authorization code from auth server
    
    Returns:
        JsonResponse: If any error occurs, containing:
            - 400 status: For missing code or invalid token response
            - 500 status: For server communication failures
        HttpResponseRedirect: To CLIENT_LOGIN_URL (/client/login/) on success
    
    Error Cases:
        - Missing authorization code
        - Failed token exchange with auth server
        - Invalid JSON response from auth server
        - Missing access token in successful response
    """

    code = request.GET.get('code')
    
    if not code:
        return JsonResponse({'error': 'No authorization code provided'}, status=400)
    token_url = settings.TOKEN_URL  # Adjust to your auth server URL
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.CLIENT_REDIRECT_URL,
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
    }

    try:
        response = requests.post(token_url, data=payload, timeout=5, verify=settings.REQUESTS_VERIFY)
        response.raise_for_status()  # raises HTTPError if status code is 4xx or 5xx
        token_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error('Token request failed: %s', str(e))
        return JsonResponse({'error': 'Failed to contact token endpoint', 'details': str(e)}, status=500)
    except ValueError:
        logger.error('Failed to parse JSON from token response')
        return JsonResponse({'error': 'Invalid JSON from token endpoint'}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'Failed to decode token response', 'details': str(e)}, status=400)

    if 'access_token' not in token_data:
        return JsonResponse({'error': 'Failed to obtain token', 'details': token_data}, status=400)

    logger.debug('Token data received from auth server:', token_data)

    request.session['access_token'] = token_data['access_token']
    return HttpResponseRedirect('/client/login/')

def client_login(request):
    """
    Display protected resources after successful OAuth authentication.
    
    This view:
    1. Checks for a valid access token in the session
    2. Makes an authenticated request to the resource server
    3. Renders the response data in app.html template
    
    If no access token exists, redirects to the OAuth login flow.
    
    Args:
        request (HttpRequest): The incoming request object containing:
            - session 'access_token': The stored OAuth access token
    
    Returns:
        HttpResponseRedirect: To CLIENT_LOGIN_URL if no access token exists
        HttpResponse: Rendered app.html template with:
            - data_json: JSON string of resource server response
            - Or error information if request failed
    
    Error Cases:
        - Missing access token (redirects to login)
        - Resource server request failure
        - Invalid JSON response from resource server
    """
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect(settings.CLIENT_LOGIN_URL)  # or wherever makes sense

    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        resource_response = requests.get(settings.RESOURCE_URL, headers=headers, timeout=5)
        resource_response.raise_for_status()
        data = resource_response.json()
    except requests.exceptions.RequestException as e:
        logger.error('Resource request failed: %s', str(e))
        data = {'error': 'Failed to contact resource server', 'details': str(e)}
    except ValueError:
        logger.error('Failed to parse JSON from resource response')
        data = {'error': 'Invalid JSON from resource server'}

    data_json = json.dumps(data)
    return render(request, 'app.html', {
        'data_json': data_json
    })

    ##return JsonResponse(data)
def oauth_login(request):
    """
    Initiate the OAuth 2.0 authorization code flow.
    
    Redirects the user to the authorization server with required parameters:
    - response_type=code for authorization code flow
    - client_id for client identification
    - redirect_uri for callback handling
    - scope defining requested permissions
    
    Args:
        request (HttpRequest): The incoming request object
    
    Returns:
        HttpResponseRedirect: To the authorization server's authorization endpoint
                            with OAuth parameters in the query string
    
    """
    auth_url = settings.AUTH_SERVER_AUTH
    
    params = {
        'response_type': 'code',
        'client_id': settings.OAUTH_CLIENT_ID,  # Your registered client ID
        'redirect_uri': settings.CLIENT_REDIRECT_URL,
        'scope': 'read',  # Or another scope you have defined
    }

    full_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    return HttpResponseRedirect(full_url)

