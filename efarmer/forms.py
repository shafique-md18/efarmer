from django import forms


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
