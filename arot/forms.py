from django import forms 

from arot.models import ArotService


class Reserve(forms.ModelForm):
    class Meta:
        models = ArotService
        fields = ['date', 'service', 'description']

        widgets = {
            'date':forms.DateInput(attrs={'class':""}),
            'service':forms.ChoiceWidget(attrs={'class':""}), 
            'description': forms.Textarea(attrs={'class':""})
        }
