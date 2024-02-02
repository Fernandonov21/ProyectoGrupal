from django import forms


class LoginForms(forms.Form):
    Email = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput)
