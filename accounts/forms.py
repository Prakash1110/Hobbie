from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    # username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user



class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ["username","email","first_name", "last_name","profile_photo","phone_number"]

class ApplicationForm(forms.Form):
    subject = forms.CharField(
        label = 'Subject',
        max_length = 50,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control','name': 'body'})
    )   

    email = forms.EmailField(
        label = 'Email',
        max_length = 150,
        required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control','name': 'body'})
        
    )  

    message = forms.CharField(
        label = 'Message',
        max_length = 2000,
        required = True,
        widget = forms.Textarea(attrs = {'class': 'form-control','name': 'body'})
        )
   
    class Meta:
        fields = ('message','subject','email')