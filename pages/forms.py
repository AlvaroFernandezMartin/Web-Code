from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    company_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    telephone = forms.CharField(max_length=20, required=True)
    file = forms.FileField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
