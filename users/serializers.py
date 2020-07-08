from django.contrib.auth.models import User, Group
from rest_framework import serializers
from backend.serializers import LanguageSerializer
from users.models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'date_joined', 'email', 'groups', 'password']
        extra_kwards = {'password' : {'write_only': True}}


class UserGetSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'last_name', 'first_name', 'is_active', 'profile']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)
    languages_know = LanguageSerializer(many=True)
    languages_learn = LanguageSerializer(many=True)
    user = UserGetSerializer(many=False, read_only=True)
    #age = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Profile

    def get_age(self, obj):
        return obj.age
