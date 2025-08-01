# Client Service (`client_serv`)

This directory contains the **Django OAuth2 client** application, which integrates with an authorization server and a resource server to complete the OAuth 2.0 Authorization Code flow, obtain access tokens, and fetch protected resources.

---

## 🚀 Features

- **Authorization Code Flow**: Redirects users to the auth server, handles callbacks, exchanges codes for tokens.
- **Protected Resource Fetching**: Uses the access token to make authenticated requests to the resource server.
- **Error Handling & Logging**: Wraps HTTP/HTTPS calls in try/except and logs events via Django's logging system.
- **Template Rendering**: Renders fetched data in a simple HTML dashboard (`app.html`).
- **Docker­-Ready**: Includes a Dockerfile for containerization; works alongside other services via Docker Compose.

---

## 📋 Files & Directories

```
client_serv/
├── Dockerfile             # Build instructions for Docker image
├── client_app/
│   ├── views.py           # Main views: oauth_login, oauth_callback, client_login
│   └── templates/
│       └── app.html       # Dashboard template
├── client_server/
│   ├── settings.py        # Environment-backed settings (ngrok, endpoints, secrets)
│   ├── urls.py            # URL routes for login, callback, and client pages
│   └── wsgi.py            # WSGI entrypoint for Gunicorn
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .env          		   # environment variables
├── manage.py              # Django management script
└── README.md              # This documentation
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

# 2. Ensure you have a .env file at project root (see client_serv/.env.example)
cp client_serv/.env.example client_serv/.env

# 3. Launch all services (auth, resource, client) with Docker Compose
docker-compose up --build -d

# 4. Access the client at your url (ngrok)
```

The client service will automatically fetch its configuration (NGROK\_URL, OAuth credentials, etc.) from the shared `.env` and the ngrok API endpoint.


---

## 🌐 Endpoints

| URL Path           | View             | Description                                    |
| ------------------ | ---------------- | ---------------------------------------------- |
| `/login/`          | `oauth_login`    | Redirects to the auth server for login         |
| `/oauth/callback/` | `oauth_callback` | Handles the callback, exchanges code for token |
| `/client/login/`   | `client_login`   | Fetches and displays protected resources       |

---

## 📜 Testing

- No tests included by default; consider adding `client_app/tests.py` for unit and integration tests of the OAuth flow.

---

## 📖 Further Reading

- [Django Documentation](https://docs.djangoproject.com/en/5.1/)
- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [python-decouple](https://github.com/henriquebastos/python-decouple)

---

*Prepared for the django\_with\_oauth project.*

