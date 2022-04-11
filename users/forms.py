from django import forms
from django.contrib.auth.forms import PasswordChangeForm

# from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # username = email로 바꿔야함
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    # 위에서 아래로 cleaned되어서 데이터가 된다
    # 따라서 clean password을 사용하면 password1의 데이터를 얻을 수 없다
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # override save method
    def save(self, *args, **kwargs):
        # 오브젝트를 생성하지만 데이터베이스에 등록하고 싶지 않을 때 commmit = False사용
        # Create, but don't save the new author instance
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


class UpdatePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Current Password", "class": "form-btn rounded-t-lg"}
        ),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "New Password", "class": "form-btn"}
        ),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm New Password",
                "class": "form-btn rounded-b-lg",
            }
        ),
    )
