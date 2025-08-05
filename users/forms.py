from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

user_model = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = user_model
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if user_model.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя пользователя"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Старый пароль"}
        )
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Новый пароль"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Подтвердите новый пароль"}
        )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        if old_password and new_password1 and old_password == new_password1:
            raise forms.ValidationError(
                "Новый пароль не должен совпадать со старым паролем."
            )
        return cleaned_data

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}), 
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'avatar': forms.FileInput(attrs={'class': "form-control"}),
            'birth_date': forms.DateInput(attrs={'class': "form-control"}),
            'telegram_id': forms.TextInput(attrs={'class': "form-control"}), 
            'github_id': forms.TextInput(attrs={'class': "form-control"}),
        }

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': "form-control"}),
            'birth_date': forms.DateInput(attrs={'class': "form-control"}),
            'telegram_id': forms.TextInput(attrs={'class': "form-control"}),
            'github_id': forms.TextInput(attrs={'class': "form-control"}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label or ""

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label or ""
