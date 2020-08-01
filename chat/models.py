from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

def message_images_path(instance, filename):
    return 'messages/user_{0}/user_{1}/images/{2}'.format(instance.sender.id, instance.receiver.id, filename)


class MessageImage (models.Model):
    image_path = models.ImageField(upload_to=message_images_path)

    message = models.ForeignKey('Message', on_delete=models.CASCADE)


class DialogManager (models.Manager):
    use_for_related_fields = True

    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_new=True)
        return qs.exclude(last_message__sender=user) if user else qs


class Dialog (models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )
    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )

    participants = models.ManyToManyField(User)

    objects = DialogManager()


    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = _('dialog')
        verbose_name_plural = _('dialogs')
        ordering = ['-last_message__date']

    def __str__(self):
        l = list(self.participants.values_list('username')[:3])
        return ", ".join(list(map(lambda u: u[0], l)))


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sended")

    text = models.TextField()

    is_new = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}...'.format(self.text[:30]) if len(self.text) > 30 else self.text

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['-date']

