from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import Message


@receiver(post_save, sender=Message)
def post_save_comment(sender, instance, created, **kwargs):
    if created:
        instance.dialog.last_message = instance
        instance.dialog.save(update_fields=['last_message'])