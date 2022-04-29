import datetime

from django.db import models

# 파이썬 것이 아니라 장고의 타임존을 쓰는 이유는 나중에 장고에서 타임존을 바꿀 떄 날짜도 같이 바꿀 수 있기 때문
from django.utils import timezone
from core import models as core_models

# 예약 취소 확정 등 추가 기능 확장하기


class BetweenDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Between Day"
        verbose_name_plural = "Between Days"

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            filter__room = BetweenDay.objects.filter(reservation__room=self.room)
            existing_booked_day = filter__room.filter(day__range=(start, end)).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)

                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BetweenDay.objects.create(day=day, reservation=self)

                return

        return super().save(*args, **kwargs)
