# Resource Server 

This directory contains the Resource Server. It contains a PostgreSQL database with some sample data and can perform some privacy transformations and host the data.

---

## Features

- **Privacy transformations**: Perform transformations such as anonymization, removal, averaging, picture blurring.
- **Host data**: Hosts the data on an endpoint where it can be accessed according to the chosen privacy settings.
- **Database**: Wraps HTTP/HTTPS calls in try/except and logs events via Django's logging system.


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
| `/admin/`            | Django Admin                | Admin interface for managing users            |
| `/api/photos/`       | `protected_photos`          | Returns patient photo and biometric data based on JWT authorization        |
| `/photos/<filename>` | `django.views.static.serve` | Serves uploaded image files in development mode (`DEBUG=True`)             |


*Prepared for the django\_with\_oauth project.*

