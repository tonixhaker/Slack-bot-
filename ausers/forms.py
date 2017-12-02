from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        exclude = ['count']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        print(cleaned_data)
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
