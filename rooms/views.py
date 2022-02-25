from django.shortcuts import render
from . import models

# 파이썬 문법을 활용하여 여러 함수들을 생성하고
# 이를 이용하여 자신이 원하는 형태로 데이터를 처리한 뒤, 어떠한 html로 데이터를 보내게 됩니다.


# http response를 쓰는 것이 번거롭기 떄문에 template를 render한다
# 템플릿은 파이썬이 compile해주는 html이다
def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(
        request,
        "rooms/home.html",
        context={"rooms": all_rooms},
    )
