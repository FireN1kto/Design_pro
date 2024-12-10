from django.contrib import admin
from .models import AdvUser, InteriorDesignRequest, Category


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'login', 'email', 'status')

    list_filter = ('is_activated',)

    readonly_fields = ('username', 'full_name','first_name', 'last_name', 'login', 'date_joined')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('email',)

        return self.readonly_fields

admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(InteriorDesignRequest)
admin.site.register(Category)