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
from rest_framework import routers
from django.urls import path, include
from users import views as uv
from cards import views as cv

router = routers.DefaultRouter()
router.register(r'users', uv.UserViewSet)
router.register(r'groups', uv.GroupViewSet)
router.register(r'languages', cv.LanguageViewSet)
router.register(r'words', cv.WordViewSet)
router.register(r'themes', cv.ThemeViewSet)
router.register(r'cardsets', cv.CardsetViewSet)
router.register(r'cards', cv.CardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('user/', include("users.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework'))
]
