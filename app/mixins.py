from django.views.generic.edit import FormMixin
from django.contrib import messages

from forms.models import CommercialProposalRequest


class CustomFormMixin(FormMixin):
    def get_success_url(self):
        return self.request.path_info

    def post(self, request, *args, **kwargs):
        self.object = CommercialProposalRequest
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваша заявка принята! Мы вам перезвоним для уточнения деталей.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
