from django.urls import path
from . import views

app_name = "rooms"

# path에 name을 지정해주면 어느 template에서든 간단하게 url로 연결시킬 수 있다.
urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
