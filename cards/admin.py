from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Language)
admin.site.register(Word)
admin.site.register(Theme)
admin.site.register(Cardset)
admin.site.register(Card)