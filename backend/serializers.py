from rest_framework import serializers

from cards.models import Language, Word, Theme


class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Language
        fields = ['name']


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields =  ['name']


class ThemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Theme
        fields =  ['name']