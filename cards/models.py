from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Language(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=_("Enter the language name (e.g. English, Russian, German etc.)")
    )

    def __str__(self):
        return self.name


class Word(models.Model):
    #language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=200,
        help_text=_("Enter word")
    )

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=_("Enter name of cardset name (e.g. IT, sport, music etc.)")
    )

    def __str__(self):
        return self.name


class Cardset(models.Model):
    name = models.CharField(max_length=200, help_text=_("Name of cardset"))
    from_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, related_name="from_language")
    to_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, related_name="to_language")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    theme = models.ManyToManyField('Theme', help_text=_("Theme of the cardset"))
    last_revision_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    cardset = models.ForeignKey('Cardset', on_delete=models.SET_NULL, null=True)
    native_word = models.ForeignKey('Word', on_delete=models.SET_NULL, null=True, related_name="native_word")
    translate_word = models.ForeignKey('Word', on_delete=models.SET_NULL, null=True, related_name="translate_name")

    def __str__(self):
        return '({0},{1})'.format(self.native_word.name, self.translate_word.name)