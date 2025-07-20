# Auth Server (`auth_server`)

This directory contains the **Django OAuth2 Authorization Server** component of the `django_with_oauth` project. It implements a robust OAuth2 Authorization Code flow with JWT access tokens, custom scope/policy selection, token logging, and email notifications.

---

## 🚀 Features

- **Authorization Code Flow**: Securely handle user authorization with django-oauth-toolkit’s `/o/authorize/` and `/o/token/` endpoints.
- **JWT Access Tokens**: Issue RS256-signed JSON Web Tokens via `jwt_app` for stateless, scalable authentication.
- **Custom Scopes & Policies**: Interactive consent UI (`ScopeSelectionView`) backed by `custom_scopes_and_policies_app`, storing user-selected policy levels in a custom grant model.
- **Token Logging & Notifications**: Persist token events in `obligations_app` (`OAuthTokenLog`) and send email alerts on issuance.
- **ngrok Development Support**: Auto-detect public URLs via ngrok for easy testing of OAuth redirects.
- **Docker-Ready**: Includes `Dockerfile` and works with Docker Compose for seamless multi-service orchestration.

---

## 📦 Project Structure

```text
auth_server/
├── auth_server_django/              # Django project package with settings, URLs, ASGI/WSGI setup
│   ├── settings.py                  # Django + OAuth2 + JWT + email + ngrok configuration
│   ├── urls.py                      # Main URL routing for admin and oauth2_provider endpoints
│   ├── asgi.py                      # ASGI entrypoint for asynchronous servers
│   ├── wsgi.py                      # WSGI entrypoint for traditional servers (e.g., Gunicorn)
│   └── keys/                        # RSA key-pair files: private.pem and public.pem for JWT signing
├── custom_scopes_and_policies_app/  # Django app: manages custom scopes, policy levels, grant model, validators
│   ├── validators.py                # Custom OAuth2Validator extension
│   ├── models.py                    # CustomGrant model extending AbstractGrant
│   ├── views.py                     # Scope selection view with custom consent handling
│   └── apps.py                      # Django app configuration
├── jwt_app/                         # Django app: handles JWT token generation
│   ├── jwt_generator.py             # Core JWT creation logic
│   └── apps.py                      # Django app configuration
├── obligations_app/                 # Django app: logs token events, triggers notifications
│   ├── admin.py                     # Admin site configuration for OAuthTokenLog
│   ├── apps.py                      # Django app configuration
│   ├── models.py                    # OAuthTokenLog model for auditing
│   └── custom_signal_handler.py     # Signal handler for token creation events
├── templates/                       # Shared templates (e.g., consent screen)
├── manage.py                        # Django management script (CLI)
├── .env                             # env file
├── .env.example                     # example env file
├── Dockerfile                       # Docker build file for containerizing auth_server
└── requirements.txt                 # Python dependencies list
```

---


## 🛠 Installation & Setup

This service runs as part of the overall Docker Compose setup. To get started:

```bash
# 1. Clone the repository and switch to the appropriate branch
git clone https://github.com/IvchenkoIO/django_with_oauth.git
cd django_with_oauth
# (Optional) checkout your branch, e.g. 'docker'
# git checkout docker

# 2. Ensure you have a .env file at project root (see auth_serv/.env.example)
cp auth_serv/.env.example auth_serv/.env

# 3. Launch all services (auth, resource, client) with Docker Compose
docker-compose up --build -d

# 4. Access the client at your url (ngrok)
```

The client service will automatically fetch its configuration (NGROK\_URL, OAuth credentials, etc.) from the shared `.env` and the ngrok API endpoint.


---

## ⚙️ Configuration

- **OAuth2 Settings**: In `auth_server_django/settings.py` under `OAUTH2_PROVIDER`:
  - `SCOPES` / `DEFAULT_SCOPES`
  - `POLICY_LEVELS`
  - `ACCESS_TOKEN_EXPIRE_SECONDS`
  - `ACCESS_TOKEN_GENERATOR`
  - `GRANT_MODEL` / `OAUTH2_VALIDATOR_CLASS`

- **JWT Settings**:
  - `JWT_PRIVATE_KEY`: File path to RSA private key
  - `JWT_ALGORITHM`: Signing algorithm (e.g., `RS256`)

- **Email**:
  - Configured via Django’s `EMAIL_*` settings for SMTP delivery.

---


## 🧪 Testing

> No tests provided out-of-the-box. Consider adding:
>
> - `obligations_app/tests.py` for signal handler behavior
> - `jwt_app/tests.py` for JWT generation
> - `custom_scopes_and_policies_app/tests.py` for validator logic

---

