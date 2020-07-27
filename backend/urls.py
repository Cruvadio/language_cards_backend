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
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


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

API_TITLE = 'Language Cards API'
API_DESCRIPTION = 'A Web API for language cards web-site.'

shema_view = get_schema_view(title=API_TITLE, version=1.0)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
   # path('api/v1/profile/language', uv.set_language, name='set_language'),
    path('api/v1/auth/', include("djoser.urls")),
    path('api/v1/auth/', include("djoser.urls.jwt")),
    path('api/v1/auth/blacklist/', uv.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('api/v1/friends/', uv.FriendsListAPI.as_view(), name='friends'),
    path('shema/', shema_view),
    path('docs/', include_docs_urls(title=API_TITLE,
                                    description=API_DESCRIPTION)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
