# Generated by Django 3.0.8 on 2020-07-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20200708_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'verbose_name': 'card', 'verbose_name_plural': 'cards'},
        ),
        migrations.AlterModelOptions(
            name='cardset',
            options={'verbose_name': 'card set', 'verbose_name_plural': 'card sets'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'language', 'verbose_name_plural': 'languages'},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'verbose_name': 'theme', 'verbose_name_plural': 'themes'},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'verbose_name': 'word', 'verbose_name_plural': 'words'},
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Enter the language name (e.g. English, Russian, German etc.), max symbols - 200', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(help_text='Enter name of cardset name (e.g. IT, sport, music etc.)', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(help_text='A string value that represents word, max symbols - 200', max_length=200, unique=True),
        ),
    ]
