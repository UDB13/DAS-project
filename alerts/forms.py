from django import forms
from .models import UserPreference, AlertType

class UserPreferenceForm(forms.ModelForm):
    alert_types = forms.ModelMultipleChoiceField(
        queryset=AlertType.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        required=False
    )
    class Meta:
        model = UserPreference
        fields = ['region', 'alert_types']