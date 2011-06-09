from django import forms

class ReconfirmForm(forms.Form):
    username = forms.CharField()
