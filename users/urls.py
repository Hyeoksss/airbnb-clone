from unicodedata import name
from django.urls import path
from . import views

# config에 있는 url에서 연결 가능하다
app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback", views.github_callback, name="github-callback"),
    path("login/kakao", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.conplete_verification, name="complete-verification"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
]
