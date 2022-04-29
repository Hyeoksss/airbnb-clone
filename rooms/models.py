# python

# django
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django_countries.fields import CountryField
from cal import Calendar

# third-party
from core import models as core_models

# packages


# 반복되어 사용하는 기능이다. 아이템의 이름을 설정
# roomtype amenity ficility 모두 항목(roomtype)과 아이템들을(hotel, shared, private)가진다
# 그래서 이 아이템들은 공통된 기능을 가지므로 아이템들의 같은 기능을 모은 abstractitem을 만듬
# 이름을 가지고 str = self.name 으로 설정
class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


# Photo is linked to room and room is linked to user
# class room보다 위에 있기 떄문에 foreignkey("room", on_delete)형식을 사용 (밑으로 내려줘야 하거나)
# 모델들이 많으면 ""으로 string해서 쓰는 것이 좋다.
class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    # 사진은 방에 대한 포린 키를 가진다 - 즉 photos를 통해 방이 가진 모든 사진 확인 가능
    # room.photos.all()
    # 코드를 위에서부터 아래로 읽기 때문에 class Room보다 밑으로 보내야 하지만 "Room"을 쓰면 된다
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definiton"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="test help text")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # user가 relatedname = rooms를 통해 class Room을 찾게 함
    # hyeok.rooms.all()은 hyeok가 가지는 room을 다 볼 수 있다.
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # relatedname is for target -- users.User or Roomtype
    # 예를 들어 roomtype = hotelroom이라면 hotelroom.rooms.all()를 통해 호텔룸인 룸을 다 볼 수 있다
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # amenities.rooms, facilities.rooms, house_rules.rooms
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # view admin 어디에서든 모델을 저장할 때 실행된다
    # 그래서 어드민에서만 뭔가를 저장할 경우를 원할 때를 위해 어드민은 savemodel이라는 method를 가진다
    # savemodel은 어드민을 관리할 수 있다 어느 어드민이 저장을 시도하는지
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        if len(all_reviews) > 0:
            return round(all_ratings / len(all_reviews), 1)
        else:
            return 0

    def first_photo(self):
        # want to get the value of queryset
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]
