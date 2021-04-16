from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    content = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='images', blank=True, null=True)
    share_id = models.IntegerField(null=True)
    share_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='shared_user')
    share_content = models.TextField(null=True)
    good_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-post_date',)

class Good(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_user')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='good_message')

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_user')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='share_message')

class Follow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_user')

class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_owner')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_user')
    content = models.TextField(null=True)
    action = models.TextField()
    noti_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-noti_date',)