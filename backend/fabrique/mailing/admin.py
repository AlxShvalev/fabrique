from django.contrib import admin

from .models import Client, Mailing, Message


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone_number',
        'phone_code',
        'timezone',
        'created_at',
        'edited_at',
    )
    search_fields = ('phone_number',)
    list_filter = ('phone_code',)


class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'started_at',
        'finished_at'
    )
    search_fields = ('text',)

    class Meta:
        ordered = ('started_at',)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'mailing',
        'client',
        'status',
        'sent_at'
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Message, MessageAdmin)
