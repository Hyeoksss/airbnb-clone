from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# admin을 쓰는 것과 code를 쓰는 것을 구분해야함
# admin은 유저가 접근할 수 있다
# code는 프로그래머만 접근할 수 있다 4-4 5분30초 강의 참고


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    # roomtype facility amenity all have related name = rooms
    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo


# django cities 추가하기
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    # 장고가 자동으로 방의 foreignkey를 가지고 있는 이미지를 넣는다
    # 모델에서 classPhoto는 room을 "Room"에서 가져오고 class Room이 존재하기 떄문에 알아서 매칭시켜준다
    # 즉 fk로 연결된 방을 찾아준다는 것이다
    inlines = (PhotoInline,)

    # classes collapse를 사용할 수도 있다
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "More About the Space",
            {
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # 룸의 호스트는 일반유저가 아니라 호스트여야 해서 호스트들을 필터링하는 기능을 가지는 것이다
    raw_id_fields = ("host",)

    search_fields = ("city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # obj is manager can access element
    # self is room admin class
    # obj is current row that registered in admin (#6-2 3:20)
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    # self는 class photoadmin, admin은 models.py의 class photo
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="100px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
