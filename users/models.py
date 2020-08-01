from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill

from cards.models import Language


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_('This is the user, related to this profile'))
    status = models.CharField(null=True, blank=True, max_length=200, help_text=_("Person's current mood"))

    followings = models.ManyToManyField(User, related_name="followers", blank=True)

    avatar = models.ImageField(upload_to="images/avatars/", null=True , blank=True, help_text=_('Avatar, picture'))
    avatar_small = ImageSpecField([ResizeToFill(100, 100)], format='JPEG', options={'quality': 90}, source='avatar')
    avatar_medium = ImageSpecField([ResizeToFill(300, 300)], format='JPEG', options={'quality': 90}, source='avatar')
    avatar_big = ImageSpecField([ResizeToFill(500, 500)], format='JPEG', options={'quality': 90}, source='avatar')

    birth_date = models.DateField(null=True, blank=True, help_text=_('Date, when user is born'))
    hobbies = models.CharField(max_length=200, blank=True, help_text=_('Hobbies of person, max length = 200'))
    languages_know = models.ManyToManyField(Language, related_name="know_languages", blank=True, help_text=_('Languages person already know'))
    languages_learn = models.ManyToManyField(Language, related_name='learn_languages', blank=True, help_text=_('Languages person would like to learn'))
    about_me = models.TextField(null=True, blank=True, help_text=_('Some information about person'))

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if not self.birth_date:
            return 0
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def is_followed(self, user: User):
        if user.profile.followings.filter(profile=self):
            return True
        return False

    def is_following(self, user: User):
        if self.followings.filter(id=user.id):
            return True
        return False

    def add_following(self, user: User):
        if not self.is_following(user):
            self.followings.add(user)

    def delete_following(self, user: User):
        if self.is_following(user):
            self.followings.remove(user)

    def get_friends(self):
        profiles = self.followings.filter(profile__followings=self.user).values_list('profile')
        return profiles

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


