from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from jwt import decode as jwt_decode, InvalidTokenError
from photos.models import Photo, PhotoImage, BiometricData
from datetime import datetime
from collections import defaultdict
from photos.image_processing import get_blurred_image_url
import statistics


@require_GET
def protected_photos(request):
    print(">>> photos/views.py version called")
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'No token provided'}, status=401)

    token = auth_header.split(' ')[1]
    try:
        decoded = jwt_decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
    except InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    authz = decoded.get("authorization_details", {})
    numerical_level = authz.get("numerical", "strict")
    text_level = authz.get("text", "strict")
    image_level = authz.get("images", "strict")

    # Get the latest Photo (simulate fetching user-specific record)
    try:
        photo = Photo.objects.latest("id")
    except Photo.DoesNotExist:
        return JsonResponse({"error": "No photo record found"}, status=404)

    # Apply privacy settings
    if text_level == "strict":
        name = "Anonymous"
        dob = None
    else:
        name = photo.patient_name
        dob = photo.date_of_birth.isoformat()

    images = []
    for img in photo.images.all():
        if image_level == "strict":
            blurred_url = get_blurred_image_url(img.image.path, request)
            if blurred_url:
                images.append({"url": blurred_url, "blurred": True})
            else:
                images.append({"url": request.build_absolute_uri(img.image.url), "blurred": True})
        else:
            images.append({"url": request.build_absolute_uri(img.image.url), "blurred": False})

    biometric_data = photo.biometrics.order_by("timestamp")

    if numerical_level == "strict":
        # Group by hour and average
        grouped = defaultdict(list)
        for bd in biometric_data:
            day = bd.timestamp.date()
            grouped[day].append(bd.value)

        numerical = [
            {"timestamp": day.isoformat(), "avg_heart_rate": round(statistics.mean(vals), 1)}
            for day, vals in sorted(grouped.items())
        ]
    else:
        numerical = [
            {"timestamp": bd.timestamp.isoformat(), "value": bd.value}
            for bd in biometric_data
        ]

    return JsonResponse({
        "patient": {
            "name": name,
            "date of birth": dob,
            "face_visible": photo.face_visible,
            "dummy_name_used": photo.dummy_name_used,
        },
        "images": images,
        "biometrics": numerical
    })
