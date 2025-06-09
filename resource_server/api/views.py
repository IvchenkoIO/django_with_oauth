import jwt
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path

def decode_token_from_request(request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None

    token = auth.split()[1]

    # Load public key (adjust path if needed)
    public_key_path = Path(settings.BASE_DIR) / "resource_server/keys/public.pem"
    with open(public_key_path, "r") as f:
        public_key = f.read()

    try:
        return jwt.decode(token, public_key, algorithms=["RS256"])
    except jwt.PyJWTError as e:
        print(f"JWT decode error: {e}")
        return None

def protected_photos(request):
    token_data = decode_token_from_request(request)
    if token_data is None:
        return JsonResponse({"error": "Invalid or missing token"}, status=401)

    # Extract authorization details
    authz_details = token_data.get("authorization_details", {})

    return JsonResponse({
        "message": "Token decoded successfully.",
        "authorization_details": authz_details
    })
