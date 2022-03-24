from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout

from users import models
from . import forms, models


# view 대신에 loginview를 사용하는 방법도 있따 #14-5

"""
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "hyeok@song.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})
"""

# LoginView 를 쓰면 email대신에 username을 받아와야함
# usernasme.과 email을 통일하고 싶기 때문에 FormView를 쓴다


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "hyeok@song.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # super().form_valid(form)가 호출되면 success_url로 가고 다시 작동하게 된다
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    # view를 불러올 때 url이 아직 불려지지 않음 그래서 찾을 수 없다고 에러가 나온다
    # lazy를 써서 바로 실행하지 않고 필요할 때 실행되게 만든다
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Hyeok",
        "last_name": "Song",
        "email": "hyeok@song.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def conplete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
        # django message framework
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))
