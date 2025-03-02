from django import forms


class SigninForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateu", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
