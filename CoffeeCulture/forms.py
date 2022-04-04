from django import forms
from .models import signupMaster,notes

class signupform(forms.ModelForm):
    class Meta:
        model=signupMaster
        fields='__all__'

class notesform(forms.ModelForm):
    class Meta:
        model=notes
        fields='__all__'