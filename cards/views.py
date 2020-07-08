from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from backend.serializers import WordSerializer, LanguageSerializer, ThemeSerializer
from .serializers import CardsetSerializer, CardSerializer
from .models import *
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
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CardsetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = CardsetSerializer

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

