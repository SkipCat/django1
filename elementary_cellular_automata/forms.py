from django import forms

class RuleForm(forms.Form):
    rule = forms.IntegerField(label='Enter the rule number', required=True)
