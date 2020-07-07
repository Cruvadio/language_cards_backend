from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import WordSerializer, LanguageSerializer, ThemeSerializer, CardsetSerializer, CardSerializer
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

    queryset = Cardset.objects.all()
    serializer_class = CardsetSerializer

    def get_queryset(self):
        """
        :return: list of all cardsets for the currently authenticated user.
        """
        username = self.request.query_params.get('user_id', None)
        queryset = Cardset.objects.all()
        if username is not None:
            queryset = queryset.filter(owner__id=username)
        return queryset


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer

