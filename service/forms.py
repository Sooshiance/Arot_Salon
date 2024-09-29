from django import forms 

from service.models import Rate


class UserRate(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['vote','txt']

        widget = {
            'vote': forms.NumberInput(attrs={'class':''}),
            'txt': forms.Textarea(attrs={'class':''}),
        }
