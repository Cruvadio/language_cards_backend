from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from cards.models import Language
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="images/", null=True , blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hobbies = models.CharField(max_length=200, blank=True)
    languages_know = models.ManyToManyField(Language, related_name="know_languages", blank=True)
    languages_learn = models.ManyToManyField(Language, related_name='learn_languages', blank=True)
    about_me = models.TextField(null=True, blank=True)

    @property
    def age(self):
        return (timezone.now().date() - self.birth_date).year

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()


