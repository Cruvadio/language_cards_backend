from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Language(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=_("Enter the language name (e.g. English, Russian, German etc.), max symbols - 200"),
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')


class Word(models.Model):
    #language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=200,
        help_text=_("A string value that represents word, max symbols - 200"),
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('word')
        verbose_name_plural = _('words')


class Theme(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=_("Enter name of cardset name (e.g. IT, sport, music etc.)"),
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('theme')
        verbose_name_plural = _('themes')


class Cardset(models.Model):
    name = models.CharField(max_length=200, help_text=_("Name of cardset"))
    from_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, related_name="from_language")
    to_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, related_name="to_language")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    theme = models.ManyToManyField('Theme', help_text=_("Theme of the cardset"))
    last_revision_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('card set')
        verbose_name_plural = _('card sets')


class Card(models.Model):
    cardset = models.ForeignKey('Cardset', on_delete=models.SET_NULL, null=True)
    native_word = models.ForeignKey('Word', on_delete=models.SET_NULL, null=True, related_name="native_word")
    translate_word = models.ForeignKey('Word', on_delete=models.SET_NULL, null=True, related_name="translate_name")

    def __str__(self):
        return '({0},{1})'.format(self.native_word.name, self.translate_word.name)
    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')