from django.utils import timezone
from django.views.generic import ListView
from . import models

# 파이썬 문법을 활용하여 여러 함수들을 생성하고
# 이를 이용하여 자신이 원하는 형태로 데이터를 처리한 뒤, 어떠한 html로 데이터를 보내게 됩니다.


# http response를 쓰는 것이 번거롭기 떄문에 template를 render한다
# 템플릿은 파이썬이 compile해주는 html이다
class Homeview(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # listview add roms and page_obj to context > use super()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now
        context["now"] = now
        return context


# 같은 것을 반복하고 싶지 않고 상속을 사용하고 싶을 떈 class based view 1가지를 잘함
# 복잡한 폼을 쓰거나 여러 요소에 관한 필터링이 있다면 function based view 여러가지 가능
# 복잡한 컨트롤을 하거나 코드를 보고 싶다면 fbv
# 둘 다 더 편리한 상황이 있으므로 선택
