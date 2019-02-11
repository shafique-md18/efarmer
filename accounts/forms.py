from django import forms
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"id": "full_name", "placeholder": "Full Name",
                                                              }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email Address",
                                                            }))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Your Message",
                                                           "rows": "3",
                                                           }))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "gmail.com" not in email:
            raise forms.ValidationError("Email must be gmail.com!", code="email error")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords Must Match!", code="password mismatch")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists!", code="existing email")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username taken!", code="existing username")
        return username

