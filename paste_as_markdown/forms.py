from django import forms

class MarkdownForm(forms.Form):
    content = forms.CharField(
        label='Your Markdown content',
        widget=forms.Textarea(attrs={ 'rows': 45, 'cols': 220 }),
        required=True
    )
    alias = forms.CharField(label='Custom alias (optional):', required=False)
