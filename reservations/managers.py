# manager은 objects.get, filter 등을 말한다
from django.db import models


class CustomReservationManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
