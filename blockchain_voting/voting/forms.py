from django import forms
from .models import *

from django import forms
from .models import Student, ValidAdmissionNumber

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['admission_number', 'password', 'confirm_password']

    def clean_admission_number(self):
        admission_number = self.cleaned_data.get('admission_number')
        # Check if the admission number exists in the ValidAdmissionNumber model
        if not ValidAdmissionNumber.objects.filter(admission_number=admission_number).exists():
            raise forms.ValidationError("Invalid admission number. Please ensure your admission number is valid.")
        return admission_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



class StudentLoginForm(forms.Form):
    admission_number = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)        


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
