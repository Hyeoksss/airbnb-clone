from csv import list_dialects
from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    list_display = ("__str__", "rating_average")
