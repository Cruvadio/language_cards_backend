from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Message, Dialog
from users.models import Profile


class ProfileDialogsSerializer (serializers.ModelSerializer):
    avatar_small = serializers.ImageField()
    class Meta:
        fields = ['avatar_small']
        model = Profile


class UserMessagesSerializer(serializers.ModelSerializer):
    profile = ProfileDialogsSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class MessagesSerializerGet (serializers.ModelSerializer):
    sender = UserMessagesSerializer()


    class Meta:
        fields = '__all__'
        model = Message


class MessagesSerializerPost (serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    dialog = serializers.PrimaryKeyRelatedField(queryset=Dialog.objects.all())
    class Meta:
        fields = ['text', 'sender', 'dialog']
        model = Message


class DialogsSerializer (serializers.ModelSerializer):
    participants = UserMessagesSerializer(many=True)
    last_message = MessagesSerializerGet()
    class Meta:
        fields = ['id', 'type', 'participants', 'last_message']
        model = Dialog



class DialogsSerializerDetail (serializers.ModelSerializer):
    participants = UserMessagesSerializer(many=True)
    messages = MessagesSerializerGet(many=True)
    class Meta:
        fields = '__all__'
        model = Dialog


class DialogsSerializerPost (serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        fields = ['participants', 'type']
        model = Dialog


