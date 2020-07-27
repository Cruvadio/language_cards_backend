from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import Profile
from cards.models import Language


class UserCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'password']
        extra_kwards = {'password' : {'write_only': True}}


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserGetSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'last_name', 'first_name', 'is_active', 'profile']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProfileSerializerDetail(serializers.ModelSerializer):
    avatar_small = serializers.ImageField(read_only=True)
    avatar_medium = serializers.ImageField(read_only=True)
    avatar_big = serializers.ImageField(read_only=True)

    languages_know = serializers.SlugRelatedField(queryset=Language.objects.all().order_by('name'), slug_field='name', many=True, required=False)
    languages_learn = serializers.SlugRelatedField(queryset=Language.objects.all().order_by('name'), slug_field='name', many=True, required=False)
    user = UserGetSerializer(many=False, read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        exclude = ['avatar', 'followings']
        model = Profile


    def get_age(self, obj):
        return obj.age

class ProfileEditSerializerDetail(serializers.ModelSerializer):

    class Meta:
        fields = ['birth_date', 'hobbies', 'about_me']
        model = Profile

    def get_age(self, obj):
        return obj.age


class ProfileSerializer (serializers.ModelSerializer):
    avatar_small = serializers.ImageField(use_url=True)
    user = UserGetSerializer(many=False, read_only=True)
    is_followed = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'avatar_small', 'user', 'is_followed']
        model = Profile

    def get_is_followed (self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return obj.is_followed(user)
        return False



class PhotosProfileSerializer (serializers.HyperlinkedModelSerializer):
    avatar_small = serializers.ImageField()
    avatar_medium = serializers.ImageField()
    avatar_big = serializers.ImageField()
    class Meta:
        fields = ['avatar_small', 'avatar_medium', 'avatar_big']
        model = Profile