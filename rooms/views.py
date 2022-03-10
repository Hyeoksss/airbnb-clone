from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


# 파이썬 문법을 활용하여 여러 함수들을 생성하고
# 이를 이용하여 자신이 원하는 형태로 데이터를 처리한 뒤, 어떠한 html로 데이터를 보내게 됩니다.

# django는 request를 받으면 view에서 파이썬문법을 이용해 respond함
# 매번 http response를 쓰는 것이 번거롭기 떄문에 template를 render한다
# 템플릿은 파이썬이 compile해주는 html이다
class Homeview(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# 같은 것을 반복하고 싶지 않고 상속을 사용하고 싶을 떈 class based view 1가지를 잘함
# 복잡한 폼을 쓰거나 여러 요소에 관한 필터링이 있다면 function based view 여러가지 가능
# 복잡한 컨트롤을 하거나 코드를 보고 싶다면 fbv
# 둘 다 더 편리한 상황이 있으므로 선택


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", "0"))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.get("amenities")
    f_facilities = request.GET.get("facilities")
    print(s_amenities, f_facilities)
    # request를 통해 받는 정보
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    # database를 통해 받는 정보
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
