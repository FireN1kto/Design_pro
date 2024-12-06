from django.contrib import admin
from .models import AdvUser

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'login', 'email', 'activation_status')

    list_filter = ('is_activated',)

    def activation_status(self, obj):
        return obj.activation_status()

    activation_status.short_description = 'Статус'

admin.site.register(AdvUser, AdvUserAdmin)
