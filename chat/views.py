from django.contrib.auth.models import AnonymousUser, User
from django.utils.translation import ugettext as _
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Message, Dialog
from chat.serializers import MessagesSerializerGet, DialogsSerializer, \
    DialogsSerializerPost


class MessagesList(ListCreateAPIView):

    queryset = Message.objects.all().order_by('-date')
    serializer_class = MessagesSerializerGet

    permission_classes = [IsAuthenticated]
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = MessageFilter

    def get_queryset(self):
        sel = self.kwargs['sel']
        user = self.request.user

        try:
            dialog = Dialog.objects.get(id=sel)

            if user in dialog.participants.all():
                return dialog.message_set.all()
            return None
        except Dialog.DoesNotExist:
            return None


    def post (self, request, *args, **kwargs):
        user = request.user
        sel = kwargs['sel']
        text = request.data['text']
        try:
            dialog = Dialog.objects.get(id=sel)
        except Dialog.DoesNotExist:
            return Response ({'message': _('Requested dialog not found')}, status=status.HTTP_404_NOT_FOUND)

        if user in dialog.participants.all():
            message = Message.objects.create(
                sender=user, dialog=dialog, text=text
            )
            return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)

        return Response({'message': 'You are not allowed to send message to this chat!'}, status=status.HTTP_403_FORBIDDEN)




class DialogsViewSet(viewsets.ModelViewSet):

    queryset = Dialog.objects.all()
    serializer_class = DialogsSerializer

    def get_queryset(self):
        user = self.request.user
        if type(user) == AnonymousUser:
            return Dialog.objects.all()
        return Dialog.objects.filter(participants=user).exclude(last_message__isnull=True).order_by('-last_message__date')

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return DialogsSerializerPost
        return DialogsSerializer


    def create(self, request, *args, **kwargs):
        data = request.data
        users = data["participants"]
        type = data['type']
        dialog = Dialog.objects.filter(type=type)
        for user in users:
            dialog = dialog.filter(participants=user)
        if dialog:
            return Response({"message" : "Dialog is already exists!"}, status=status.HTTP_302_FOUND)
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
