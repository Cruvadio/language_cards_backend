from rest_framework import serializers

from core.serializers import LanguageSerializer
from .models import *





class CardsetHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cardset
        fields = '__all__'


class CardsetSerializer(serializers.ModelSerializer):
    to_language = LanguageSerializer(many=False)
    from_language = LanguageSerializer(many=False)
    #owner = UserGetSerializer(many=False)
    theme = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Theme.objects.all())

    class Meta:
        model = Cardset
        fields = '__all__'




class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'