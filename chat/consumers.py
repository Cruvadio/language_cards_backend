# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import  WebsocketConsumer
from rest_framework.fields import ImageField

from backend import settings
from .models import Dialog, Message
from .serializers import MessagesSerializerGet


class Errors:
    SUCCESS = 0
    NOT_FOUND = 1
    NOT_AUTHORIZED = 2

HOST = 'http://localhost:8000'

class ChatConsumer(WebsocketConsumer):



    def get_messages(self, dialog_id, page, page_size):
        dialog = Dialog.objects.get(id=dialog_id)
        count = page * page_size
        return self.serialize_messages(dialog.message_set.all()[count-page_size:count])

    def serialize_messages(self, messages):
        data = []
        for message in messages:
            data.append(self.serialize_message(message))
        return data

    def serialize_message(self, message):
        ava = str(message.sender.profile.avatar_small)

        message = MessagesSerializerGet(message).data
        if settings.DEBUG:
            if ava:
                url = HOST + '/media/' + ava.replace("\\", '/')

                sender = message['sender']
                profile = sender['profile']
                profile['avatar_small'] = url
                sender['profile'] = profile
                message['sender'] = sender
        return message

    def send_messages(self, dialog_id, page, page_size):
        messages = self.get_messages(dialog_id, page, page_size)

        content = {
            'action': 'LOAD_MESSAGES',
            'payload': {
                'messages': messages,
                'next_page': page + 1
            }
        }

        self.send_data(content)

    def load_messages(self, payload):
        dialog_id = payload['dialog']
        page = payload['page']
        page_size = payload['page_size']

        self.send_messages(dialog_id, page, page_size)


    def new_message(self, text):
        return Message.objects.create(text=text, sender=self.scope['user'], dialog_id=int(self.room_name))


    def add_message(self, payload):
        text = payload['text']
        new_message = self.new_message(text)
        content = {
            'action': 'ADD_MESSAGE',
            'payload': {
                'message': self.serialize_message(new_message)
            }
        }

        self.broadcast_data(content['action'], content['payload'])

    def get_message(self, id):
        try:
            message = Message.objects.get(id=id)
            message.is_new = False
            message.save()
            return Errors.SUCCESS
        except Message.DoesNotExist:
            return Errors.NOT_FOUND


    def read_message(self, payload):
        message_id = payload['message']
        error = self.get_message(message_id)
        if error:
            content = {
                'action': 'READ_MESSAGE',
                'result': error,
            }
        else:
            content = {
                'action': 'READ_MESSAGE',
                'payload': payload
            }
        self.send_data(content)


    actions = {
        'ADD_MESSAGE': add_message,
        'LOAD_MESSAGES': load_messages,
        'READ_MESSAGE': read_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['sel']
        self.room_group_name = 'chat_%s' % self.room_name

        error = self.get_dialog(self.room_name)
        # Join room group
        if not error:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            self.close(code=error)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def get_dialog(self, room_id):
        user = self.scope['user']
        if user:
            try:
                dialog = Dialog.objects.get(id=int(room_id))

                if user in dialog.participants.all():
                    return Errors.SUCCESS
                return None
            except Dialog.DoesNotExist:
                return Errors.NOT_FOUND
        return Errors.NOT_AUTHORIZED

    def receive(self, text_data):
        data = json.loads(text_data)
        self.actions[data['action']](self, payload=data['payload'])

    def send_data(self, payload):
        self.send(text_data=json.dumps(payload))

    def broadcast_data(self, action, payload):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_broadcast_data',
                'action': action,
                'payload': payload
            }
        )

    def send_broadcast_data(self, event):
        payload = event['payload']
        action = event['action']
        self.send(text_data=json.dumps({
            'action': action,
            'payload': payload
        }))