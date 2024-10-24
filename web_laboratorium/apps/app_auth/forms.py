from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import validate_ums_student_email
from django.contrib.auth import get_user_model

User = get_user_model()

class UMSUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Name",
        max_length=150,
        help_text="Nama lengkap",
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        help_text="Email UMS",
        validators=[validate_ums_student_email]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'email', 'password1', 'password2', "angkatan"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_ums_student_email(username)
        username = super().clean_username()
        return username

class UMSUserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UMSUserChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("Password tidak sama")
        cleaned_data['password'] = new_password
        return cleaned_data