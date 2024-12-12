from django.contrib import admin
from .models import AdvUser, InteriorDesignRequest, Category


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'login','email', 'status')

    readonly_fields = ('username', 'login','full_name','first_name', 'last_name', 'date_joined')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('email',)

        return self.readonly_fields

admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(InteriorDesignRequest)
admin.site.register(Category)