from django.db import models
from authentication.models import LqUser
from django.utils import timezone

# Create your models here.


def event_banner(instance,filename):
    return "".join(["%s%s%s" %("media/events/banners/",int(timezone.now()),"/"),filename])


def event_video(instance,filename):
    return "".join(["%s%s%s" %("media/events/video/",int(timezone.now()),"/"),filename])


class LqEvent(models.Model):
    EVENT_STATUS=(
        (1,"Active"),
        (2,"Inactive")
    )
    name = models.CharField(max_length=255)
    host = models.ForeignKey("authentication.LqUser",on_delete=models.CASCADE,name="host_events")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255)
    banner = models.ImageField(upload_to=event_banner,null=True)
    video = models.FileField(upload_to=event_video,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=510)
    status = models.PositiveIntegerField(choices=EVENT_STATUS,default=1)

    class Meta:
        db_table = "lq_event"


def comment_image(instance,filename):
    return "".join(["%s%s%s" % ("media/events/comments/", int(timezone.now()), "/"), filename])


def comment_video(instance,filename):
    return "".join(["%s%s%s" % ("media/events/comments/", int(timezone.now()), "/"), filename])


class LqEventComments(models.Model):
    event = models.ForeignKey(LqEvent,on_delete=models.CASCADE,name="event_comments")
    user = models.ForeignKey("authentication.LqUser", on_delete=models.CASCADE, name="user_comments")
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to=comment_image, null=True)
    video = models.FileField(upload_to=comment_video,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lq_event_comments"


class LqEventLikes(models.Model):
    event = models.ForeignKey(LqEvent, on_delete=models.CASCADE, name="event_likes")
    user = models.ForeignKey("authentication.LqUser", on_delete=models.CASCADE, name="user_event_likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lq_event_likes"


class LqInterestedUser(models.Model):
    user = models.ForeignKey("authentication.LqUser", on_delete=models.CASCADE, name="interested")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lq_interested_user"


class LqGoing(models.Model):
    user = models.ForeignKey("authentication.LqUser", on_delete=models.CASCADE, name="going")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lq_going"


class LqEventCategory(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lq_event_category"

