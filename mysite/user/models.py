from django.db import models
from django.utils import timezone
from django.urls import reverse
from postsite.models import User

class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    post_user  = models.ForeignKey(User, on_delete=models.PROTECT, related_name='post_user', null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.CharField('カテゴリーの中の細かい分野', max_length=255, blank=True)
    title = models.CharField('タイトル', max_length=255)
    book_title = models.CharField('使用している本の名前', max_length=255)
    content = models.TextField('本文')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', default=None, blank=True )
    like_count = models.BigIntegerField(default='0')


    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('user:mypage')

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    no = models.IntegerField(default=0)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:25]

    class Meta:
        ordering = ['-created_at']

class CommentReply(models.Model): #コメント返信用のmodel
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_user = models.ForeignKey(User, on_delete=models.PROTECT)
    no = models.IntegerField(default=0)
    comment_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_reply[:15]

