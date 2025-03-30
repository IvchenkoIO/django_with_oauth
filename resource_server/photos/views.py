from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import jwt
from django.conf import settings

@require_GET
def protected_photos(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return JsonResponse({'error': 'No token provided'}, status=401)

    token = auth_header.split(' ')[1]  # Expects 'Bearer <token>'

    try:
        # Verify using the public key instead of a shared secret.
        decoded = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # If token is valid, return the protected resource.
    photos = [
        {'id': 1, 'title': 'Sunset', 'url': 'http://example.com/sunset.jpg'},
        {'id': 2, 'title': 'Mountain', 'url': 'http://example.com/mountain.jpg'},
    ]
    return JsonResponse({'photos': photos})
