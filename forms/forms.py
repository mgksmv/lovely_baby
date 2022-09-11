from django import forms

from .models import CommercialProposalRequest


class CommercialProposalRequestForm(forms.ModelForm):
    class Meta:
        model = CommercialProposalRequest
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя или название компании'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Введите номер или email'}),
        }
