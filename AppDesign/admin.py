from django.contrib import admin
from .models import AdvUser, InteriorDesignRequest, Category


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'login', 'email', 'status')

    list_filter = ('is_activated',)

admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(InteriorDesignRequest)
admin.site.register(Category)