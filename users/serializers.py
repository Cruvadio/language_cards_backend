from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'date_joined', 'email', 'groups', 'password']
        extra_kwards = {'password' : {'write_only': True}}


class UserGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'last_name', 'first_name', 'is_active']



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
