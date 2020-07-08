"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from backend import settings
from users import views as uv
from cards import views as cv

router = routers.DefaultRouter()
router.register(r'users', uv.UserViewSet)
router.register(r'groups', uv.GroupViewSet)
router.register(r'languages', cv.LanguageViewSet)
router.register(r'words', cv.WordViewSet)
router.register(r'themes', cv.ThemeViewSet)
router.register(r'cardsets', cv.CardsetViewSet, basename="Cardset")
router.register(r'cards', cv.CardViewSet)
router.register(r'profiles', uv.ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    #path('auth/', include("users.urls")),
    path('auth/', include("djoser.urls")),
    path('auth/', include("djoser.urls.jwt")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
