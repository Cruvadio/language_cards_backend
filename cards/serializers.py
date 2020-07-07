from rest_framework import serializers
from .models import *


class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class ThemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class CardsetHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cardset
        fields = '__all__'


class CardsetSerializer(serializers.ModelSerializer):
    to_language = serializers.StringRelatedField(many=False)
    from_language = serializers.StringRelatedField(many=False)
    owner = serializers.StringRelatedField(many=False)
    theme = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cardset
        fields = '__all__'




class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'