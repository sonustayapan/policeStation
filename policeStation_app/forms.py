from django import forms

class UsersRegistration(forms.Form):
    full_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)