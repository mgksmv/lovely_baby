from django.contrib import admin

from .models import CommercialProposalRequest


@admin.register(CommercialProposalRequest)
class CommercialProposalRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'date_created']
    readonly_fields = ['name', 'contact', 'date_created']

    def has_add_permission(self, request, obj=None):
        return False
