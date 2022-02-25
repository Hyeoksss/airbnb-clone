from django.urls import path
from rooms import views as room_views

# /rooms로 시작하는 url -> room file || start from nothing(home login logout) -> core
app_name = "core"

# 맨 처음 화면에 방들을 보여주고 싶은거니까 room을 import - > home화면에 보여줌
urlpatterns = [
    path("", room_views.all_rooms, name="home"),
]
