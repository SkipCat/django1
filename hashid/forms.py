from django import forms

class HashForm(forms.Form):
    value = forms.CharField(label='Hash value:', required=True)
