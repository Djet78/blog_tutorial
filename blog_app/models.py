from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted', ]

    def get_absolute_url(self):
        """ Redirect user to 'post_detail' of currently created post"""
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
