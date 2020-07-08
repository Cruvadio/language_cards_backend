from rest_framework import serializers

from backend.serializers import LanguageSerializer, ThemeSerializer
from users.serializers import UserGetSerializer
from .models import *





class CardsetHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cardset
        fields = '__all__'


class CardsetSerializer(serializers.ModelSerializer):
    to_language = LanguageSerializer(many=False)
    from_language = LanguageSerializer(many=False)
    #owner = UserGetSerializer(many=False)
    theme = ThemeSerializer(many=False)

    class Meta:
        model = Cardset
        fields = '__all__'




class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'