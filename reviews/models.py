from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models


# Create your models here.
class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    # 이 함수를 모든 곳에 포함시키고 싶다면 모델에 함수를 만들어서 사용한다(어드민만을위한함수와는다르다)
    # 즉 함수를 실제 사용자들이 보는 페이지에도 쓰고 싶으면 모델에서 만들어야함
    # str함수를 list display에 쓸 수 있다, 커스텀함수를 모델에다 생성할 수 있다
    # 어드민에서만 평균을 보이게 할려면 어드민에다가 쓰면 된다 그러나 이 리뷰값을 다른 곳에서도 쓸 것이기 때문에
    # 모델에 작성한다
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 1)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)


validators = []
