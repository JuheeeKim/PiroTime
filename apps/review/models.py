from django.db import models
from django.conf import settings

# 리뷰 모델
class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    giturl = models.URLField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='review_likes', 
        blank=True
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='review_bookmarks', 
        blank=True
    )

    def total_likes(self):
        return self.likes.count()
    def total_bookmark(self):
        return self.bookmarks.count()

    def __str__(self):
        return self.title

# 리뷰에 대한 댓글 모델
class Comment(models.Model):
    review = models.ForeignKey(
        Review, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='review_comments'
    )
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.writer} on {self.review}'