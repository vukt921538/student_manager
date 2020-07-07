from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='post_img', null=True, blank=True)
    like = models.ManyToManyField(User, related_name='like_user', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike_user',blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_box = models.TextField()
    date_comment = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Comment_to_comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment = models.TextField()
    date_comment = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.from_comment.comment_box

class Points(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    