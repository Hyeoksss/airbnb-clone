from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django_countries import countries
from . import models, forms


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


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                rooms = models.Room.objects.filter(**filter_args)

        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/search.html",
            {"form": form, "rooms": rooms},
        )
