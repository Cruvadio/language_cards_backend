from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django_filters import rest_framework as filters

from chat.filters import MessageFilter
from chat.models import Message, Dialog
from chat.serializers import MessagesSerializerGet, MessagesSerializerPost, DialogsSerializerDetail, DialogsSerializer, \
    DialogsSerializerPost


class MessagesViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all().order_by('-date')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return MessagesSerializerGet
        if self.action == 'create':
            return MessagesSerializerPost
        return MessagesSerializerGet


class DialogsViewSet(viewsets.ModelViewSet):

    queryset = Dialog.objects.all()
    serializer_class = DialogsSerializerDetail

    def get_queryset(self):
        user = self.request.user
        if type(user) == AnonymousUser:
            return Dialog.objects.all()
        return Dialog.objects.filter(participants=user).exclude(last_message__isnull=True).order_by('-last_message__date')

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return DialogsSerializer
        if self.action == 'create':
            return DialogsSerializerPost
        return DialogsSerializerDetail
