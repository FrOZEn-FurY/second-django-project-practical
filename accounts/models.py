from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class PostModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'posts')
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_updated',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('accounts:PostDetail', args=(self.id, self.slug))

    def like_count(self):
        return self.plike.count()

class FollowUnFollowModel(models.Model):
    FollowerUser = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'Follower')
    FollowedUser = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'Following')

    def __str__(self):
        return f'{ self.FollowedUser.username } is following { self.FollowedUser.username }'

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.user } commented on { self.post } at { self.date_created }'

class LikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='plike')

    def __str__(self):
        return f'{ self.user } liked { self.post }'

class GeneralInfoModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='GeneralInfo')
    age = models.PositiveSmallIntegerField()
    bio = models.TextField()