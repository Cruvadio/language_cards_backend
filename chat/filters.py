from django_filters import rest_framework as filters

from chat.models import Message, Dialog


class MessageFilter(filters.FilterSet):
    sel = filters.NumberFilter(method='filter_messages', required=True)

    class Meta:
        model  = Message
        fields = ['sel']

    def filter_messages (self, queryset, name, value):
        try:
            user = self.request.user
            dialog = Dialog.objects.get(id=value)
            if user in dialog.participants.all():
                return dialog.message_set.all()
            return dialog.message_set.all() # TODO DELETE THIS STRING
        except Dialog.DoesNotExist:
            return None
        return None