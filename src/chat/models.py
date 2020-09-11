from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    author = models.ForeignKey(User, related_name='my_message', on_delete=models.CASCADE)
    content = models.TextField()
    msg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + "__" + self.content[:10]

    def get_10_message():
        return Message.objects.order_by('-msg-date').all()[:10]