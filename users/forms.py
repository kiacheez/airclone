from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        try: 
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Incorrect password"))
        except:
            models.User.DoesNotExist
            self.add_error("email", forms.ValidationError("User does not exist"))

class SignUpForm(forms.ModelForm):

    class Meta:

        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First name"}),
            'last_name': forms.TextInput(attrs={"placeholder": "Last name"}),
            'email': forms.EmailInput(attrs={"placeholder": "Email address"})
        }
       
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}), label="Confirm Password" )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 메일주소입니다.", code="existing_user")

        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호를 확인해주세요.")

        else:
            return password

    def save(self, *arg, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email") 
        password = self.cleaned_data.get("password")
        user.username =email
        user.set_password(password)
        user.save()