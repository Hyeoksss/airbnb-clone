from django.urls import path, reverse_lazy
from . import views

# config에 있는 url에서 연결 가능하다
app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:key>/", views.conplete_verification, name="complete-verification"
    ),
    path("update_profile", views.UpdateProfileView.as_view(), name="update"),
    path(
        "update_password",
        views.UpdatePasswordView.as_view(success_url=reverse_lazy("core:home")),
        name="password",
    ),
    path("switch-hosting", views.switch_hosting, name="switch-hosting"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
]
