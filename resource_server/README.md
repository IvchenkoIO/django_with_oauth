# Resource Server

This directory contains the Resource Server. It includes a PostgreSQL database with sample data, offers privacy transformations, and hosts the data for access.

---

## Features

- **Privacy transformations**: Anonymization, removal, averaging, image blurring.
- **Host data**: Serves data on an endpoint with authorization and privacy settings.
- **Database**: Stores patient data in PostgreSQL.

---

## Files & Directories

└───resource_server
    │   Dockerfile      # Build instructions for Docker image
    │   entrypoint.sh   # Container entrypoint script for setup and startup
    │   manage.py       # Django management script
    │   README          # Documentation
    │
    ├───api
    │       urls.py     # more endpoint definitions
    │
    ├───photos
    │   │   image_processing.py     # Image blurring
    │   │   models.py               # Data model definition
    │   │   privacy_config.py       # Privacy level mappings
    │   │   views.py                # Main view: protected_photos(), returns authorized data
    │   │
    │   ├───management
    │   │   ├───commands
    │   │   │   │   seed_photos.py      # Generates test data
    │   │
    │   ├───migrations
    │   │   │   0001_initial.py         # Initial model migration and model changes
    │   │   │   ...
    │   │   │
    │   ├───photos                      # Photos get stored here
    │   │   ├───blurred
    │   │   └───originals
    │   │
    │   ├───test_assets                 # Sample images
    │   │       checkup.jpg
    │   │       profile.jpg
    │   │       surgery.jpg

    ├───resource_server
    │   │   settings.py                 # Django settings
    │   │   urls.py                     # URL routing
    │   │

## Endpoints

| URL Path             | View                        | Description                                                                |
| -------------------- | --------------------------- | -------------------------------------------------------------------------- |
| `/admin/`            | Django Admin                | Admin interface for managing users            
| `/api/photos/`       | `protected_photos`          | Returns patient photo and biometric data based on JWT authorization        |
| `/photos/<filename>` | `django.views.static.serve` | Serves uploaded image files in development mode (`DEBUG=True`)             |


## Tests

Tests were done manually by generating different tokens for the different modes and accessing the endpoint with a PowerShell's Invoke-WebRequest while measuring the time.
After every test, the resource_server was restarted. Otherwise response times go down ~20%, which could be attributed to warmup effects such as cache hits.
If the resource server is left idle for a while, response time increases by about 0.2 seconds. In rare instances, access time was more than 3 seconds, which is very different from the usual 0.3 - 0.8 seconds. To achieve comparability, and since the purpose of these tests was the performance of the actual transformations, all tests were done exactly 30 seconds after restart.


An example is pictured below:

Go to:
https://privacyengproj.ngrok.app/auth/o/authorize/?client_id=um4sg4XLnZ1XNttK64bVFySS071Pghi9hUVnkrsc&response_type=code&redirect_uri=https%3A%2F%2Fprivacyengproj.ngrok.app%2Fclient%2Foauth%2Fcallback%2F&scope=read&authorization_details={%22average%20numerical%20values?%22:%22none%22,%22blur%20images?%22:%22none%22,%22transform%20text?%22:%22none%22}

Retreive access code

Run from terminal:
$response = Invoke-WebRequest "https://privacyengproj.ngrok.app/auth/o/token/" `
  -Method POST `
  -Body @{
    grant_type    = "authorization_code"
    code          = "Pw9qxwrjlBSUW7vW0IrkeWmic2u1C6"  
    redirect_uri  = "https://privacyengproj.ngrok.app/client/oauth/callback/"
    client_id     = "um4sg4XLnZ1XNttK64bVFySS071Pghi9hUVnkrsc"
    client_secret = "Wzv0PuOiJEx16a9xr7FCkHab11B5LKzyQyXs8oYWsADK9vFiYMvwF0n3rZXTJ97WZtxPec6cuS1PD0kQlfUZY0lR0AplGvOL2XJJpRwe963N9UrF9ID159PnzLcjq6aZ"
  } `
  -UseBasicParsing

# View the token:
($response.Content | ConvertFrom-Json).access_token

Retreive token

Run from terminal:
$token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzUzMDA3MTIyLCJleHAiOjE3NTMwNDMxMjIsImp0aSI6ImEwYTY0ZmNmLTIxYjctNDRjNS1hM2M0LTFlNDFmZjI5NWE1OSIsInNjb3BlIjpbInJlYWQiXSwiYXV0aG9yaXphdGlvbl9kZXRhaWxzIjp7ImF2ZXJhZ2UgbnVtZXJpY2FsIHZhbHVlcz8iOiJob3VybHkiLCJibHVyIGltYWdlcz8iOiJoZWF2eSIsInRyYW5zZm9ybSB0ZXh0PyI6ImFub255bWl6ZSJ9fQ.7TEFpo1utfdhWOWAxUSmRQBwhJFEb4dWf1qDoDpXQv6Twm-KAMz87TMCGEiRB8751x_zvv-QyjnmAX5O-E9mfyHqIBKcGoqNwYBlQVzxzGWSrYHpUZgH8Kk89W8Ed-o4a0ilQsBlgc7isXg-dEL6YVwV_mvbw90V6F5UfStGlhkp_7EO1-p_v8DHitROtShgrECXaclsY5798R-9bTFj-gmInXUvgq8wLsE0lVFWeFZnNfb5n5DjvV_wzYBBbFAFjsCU7MWt4yip55pKxIMClMqb4-8GzhAxgWw_25cHhrkLa0eSrFqbw6j2ABITy-NIhNs2hVXBRjyayKB_bQbKBQ"

$headers = @{ Authorization = "Bearer $token" }

$start = Get-Date
$response = Invoke-WebRequest "https://privacyengproj.ngrok.app/resource/api/photos/" -Headers $headers -UseBasicParsing
$end = Get-Date

# Output
"Status: $($response.StatusCode)"
"Elapsed time: $((($end - $start).TotalSeconds)) sec"

## Results:

### Benchmark Processing Time of Privacy Transformations (in seconds)

| numerical     | none   | hourly | daily  | none   | none   | hourly | hourly |
| images        | none   | none   | none   | mild   | strong | mild   | mild   |
| personal data | none   | none   | none   | none   | none   | none   | anonymous |
| **Values**    |        |        |        |        |        |        |        |
|---------------|--------|--------|--------|--------|--------|--------|--------|
|               | 0.365  | 0.237  | 0.273  | 0.815  | 0.907  | 0.761  | 0.789  |
|               | 0.366  | 0.237  | 0.221  | 0.808  | 0.823  | 0.695  | 0.760  |
|               | 0.371  | 0.242  | 0.204  | 0.812  | 0.792  | 0.701  | 0.685  |
|               | 0.370  | 0.233  | 0.205  | 0.799  | 0.886  | 0.699  | 0.673  |
|               | 0.369  | 0.252  | 0.218  | 0.794  | 0.915  | 0.691  | 0.707  |
|               | 0.410  | 0.225  | 0.210  | 0.807  | 0.839  | 0.699  | 0.678  |
|               | 0.354  | 0.247  | 0.221  | 0.823  | 0.801  | 0.681  | 0.670  |
|               | 0.377  | 0.235  | 0.213  | 0.815  | 0.789  | 0.721  | 0.675  |
|               | 0.400  | 0.244  | 0.220  | 0.785  | 0.870  | 0.729  | 0.679  |
|               | 0.381  | 0.267  | 0.206  | 0.823  | 0.796  | 0.676  | 0.679  |
|---------------|--------|--------|--------|--------|--------|--------|--------|
| **Average**   | 0.3763 | 0.2419 | 0.2191 | 0.8081 | 0.8418 | 0.7053 | 0.6995 |



*Prepared for the django\_with\_oauth project.*

