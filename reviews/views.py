from django.contrib import messages
from django.shortcuts import redirect, reverse
from . import forms
from rooms import models as room_models


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = forms.save(request)
            review.room = room_models
            review.user = request.user
            review.save()
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
