from django import forms


class HealthDataForm(forms.Form):
    diet = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)
    stress = forms.IntegerField(min_value=1, max_value=10, required=True)
    activity = forms.IntegerField(min_value=0, required=True)
    sleep = forms.IntegerField(min_value=0, required=True)
    biometrics = forms.CharField(required=True,
                                 help_text='Format: BP:120/80, Glucose:90')
    medications = forms.CharField(required=True)
    family_history = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=True)
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
