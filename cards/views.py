from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.serializers import WordSerializer, LanguageSerializer, ThemeSerializer
from users.models import Profile
from users.permissions import IsReadOnlyOrIsOwner
from .models import *
from .serializers import CardsetSerializer, CardSerializer


# Create your views here.


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer


class ProfileLanguagesLearn(viewsets.ModelViewSet):
    """
    View to set profile languages or delete them

    * Requires token authentication
    * Only user can change his own languages
    """
    permission_classes = [IsReadOnlyOrIsOwner, IsAuthenticated]
    serializer_class = LanguageSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Language.objects.exclude(learn_languages=profile)


class ProfileLanguagesKnow(viewsets.ModelViewSet):
    """
        View to set profile languages or delete them

        * Requires token authentication
        * Only user can change his own languages
    """
    permission_classes = [IsReadOnlyOrIsOwner, IsAuthenticated]
    serializer_class = LanguageSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Language.objects.exclude(know_languages_=profile)


class CardsetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = CardsetSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """
        :return: list of all cardsets for the currently authenticated user.
        """
        user = self.request.user
        return Cardset.objects.filter(owner=user)


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
