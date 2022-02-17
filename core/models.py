from django.db import models


class TimeStampedModel(models.Model):

    """Time Stapmed Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # TimeStampedModel을 db에 등록하지 않고 이것을 사용하는 모델을 db에 등록
    # 이러한 abstractmodel은 모델을 확장하기 위해 사용된다
    class Meta:
        abstract = True
