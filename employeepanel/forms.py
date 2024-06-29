from django import forms

class DeletionReasonForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label='Razón de eliminación')