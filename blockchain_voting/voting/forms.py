from django import forms
from .models import *

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'description', 'image']
 

class VotingTimeframeForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label="Start Time"
    )
    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label="End Time"
    )

    class Meta:
        model = VotingTimeframe
        fields = ['start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after the start time.")
