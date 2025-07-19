from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from jwt import decode as jwt_decode, InvalidTokenError
from photos.models import Photo, BiometricData
from photos.image_processing import get_blurred_image_url
from photos.privacy_config import HEART_RATE_GROUPING, DEFAULT_HEART_RATE_POLICY

from collections import defaultdict
import statistics


@require_GET
def protected_photos(request):
    print(">>> photos/views.py version called")
    
    # Extract Token
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'No token provided'}, status=401)

    token = auth_header.split(' ')[1]
    try:
        decoded = jwt_decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
    except InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # Parameters from Token
    authz = decoded.get("authorization_details", {})
    numerical_level = authz.get("average numerical values?", DEFAULT_HEART_RATE_POLICY)
    image_blur_level = authz.get("blur images?", "none")
    text_privacy_level = authz.get("transform text?", "none")

    # Get Photo
    try:
        photo = Photo.objects.latest("id")
    except Photo.DoesNotExist:
        return JsonResponse({"error": "No photo record found"}, status=404)

    # Anonymize and remove
    if text_privacy_level == "remove":
        name = None
        dob = None
    elif text_privacy_level == "anonymize":
        name = "Anonymous"
        dob = "01.01.1900"
    else:
        name = photo.patient_name
        dob = photo.date_of_birth.isoformat() if photo.date_of_birth else None

    # Image blurring here
    images = []
    for img in photo.images.all():
        if image_blur_level == "none":
            images.append({
                "url": request.build_absolute_uri(img.image.url),
                "blurred": False
            })
        else:
            blurred_url = get_blurred_image_url(img.image.path, request, blur_level=image_blur_level)
            images.append({
                "url": blurred_url if blurred_url else request.build_absolute_uri(img.image.url),
                "blurred": True
            })

    # Grouping and averaging biometrics
    biometric_data = photo.biometrics.order_by("timestamp")
    grouping = HEART_RATE_GROUPING.get(numerical_level, None)

    def group_by_interval(interval_hours):
        grouped = defaultdict(list)
        for bd in biometric_data:
            rounded = bd.timestamp.replace(minute=0, second=0, microsecond=0)
            rounded = rounded.replace(hour=(bd.timestamp.hour // interval_hours) * interval_hours)
            grouped[rounded].append(bd.value)
        return [
            {"timestamp": ts.isoformat(), "avg_heart_rate": round(statistics.mean(vals), 1)}
            for ts, vals in sorted(grouped.items())
        ]

    if grouping is None:
        numerical = [
            {"timestamp": bd.timestamp.isoformat(), "value": bd.value}
            for bd in biometric_data
        ]
    elif grouping == "daily":
        grouped = defaultdict(list)
        for bd in biometric_data:
            grouped[bd.timestamp.date()].append(bd.value)
        numerical = [
            {"timestamp": day.isoformat(), "avg_heart_rate": round(statistics.mean(vals), 1)}
            for day, vals in sorted(grouped.items())
        ]
    else:
        numerical = group_by_interval(grouping)
        
    # Grouping and averaging biometrics
    return JsonResponse({
        "patient": {
            "name": name,
            "date of birth": dob,
        },
        "images": images,
        "biometrics": numerical
    })
