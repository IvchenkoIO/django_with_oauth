"""
URL configuration for auth_server_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


"""
--------------------------

Root URL configuration for the OAuth2 Authorization Server.

Routes:
    /auth/admin/     → Django admin site
    /auth/o/         → django-oauth-toolkit endpoints (authorize, token, revoke, introspect, jwks, etc.)

"""
from django.contrib import admin
from django.urls import include,path
from oauth2_provider import urls as oauth2_urls
from custom_scopes_and_policies_app.views import ScopeSelectionView
urlpatterns = [
    # Admin site (login, user management, client registration)
    path('admin/', admin.site.urls),
    # OAuth2 endpoints:
    #   - /o/authorize/   (Authorization Code, Implicit, etc.) -> we will be using our custom forms for that so we change the url as well
    #   - /o/token/       (Token exchange)
    path('o/', include(oauth2_urls, namespace='oauth2_provider')),
    path('auth', ScopeSelectionView.as_view(),name="select_scopes"),
]
