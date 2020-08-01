from django.contrib import admin

# Register your models here.
from chat.models import Message, Dialog

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'sender', 'date')

class DialogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['participants']
    search_fields = ('participants',)
    actions = ['fix_last_messages']

    def fix_last_messages(self, request, queryset):
        for dialog in queryset.all():
            dialog.last_message = dialog.message_set.all().order_by('-date').first()
            dialog.save(update_fields=['last_message'])

    fix_last_messages.short_description = 'Fix last messages'

admin.site.register(Message, MessageAdmin)
admin.site.register(Dialog, DialogAdmin)