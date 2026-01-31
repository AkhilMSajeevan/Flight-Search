from django import forms
from .model import AirportRoute

class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ['parent_airport', 'airport_code', 'position', 'duration']
        widgets = {
            'airport_code': forms.TextInput(attrs={'required': 'required'}),
            'position': forms.Select(attrs={'required': 'required'}),
            'duration': forms.NumberInput(attrs={'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].initial = 'Left'

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent_airport')
        position = cleaned_data.get('position')
        if parent and position:
            # Check if a child with this position already exists for this parent
            exists = AirportRoute.objects.filter(parent_airport=parent, position=position).exists()
            if exists:
                raise forms.ValidationError(
                    f"This parent airport already has a {position.lower()} airport."
                )
        return cleaned_data
    
class SearchForm(forms.Form):
    airport = forms.ModelChoiceField(queryset=AirportRoute.objects.all(), required=True, label="Select Airport")
    direction = forms.ChoiceField(choices=[("Left", "Left"), ("Right", "Right")], required=True, label="Direction")