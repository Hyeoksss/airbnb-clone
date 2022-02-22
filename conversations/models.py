from django.db import models
from core import models as core_models

# trip model 만들기 #5-3 2:10 참고


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    # conversation은 message라는 foriegn key를 가짐 즉 conversation에서 relatedname = messages
    # 를 통해서 message에 접근할 수 있다
    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
