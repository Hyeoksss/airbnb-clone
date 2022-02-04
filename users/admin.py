from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class CunstomUserAdmin(admin.ModelAdmin):

    """Custom User Admin"""

    list_display = ("username", "gender", "language", "currency", "superhost")
    list_filter = ("superhost",)
