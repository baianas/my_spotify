from django.db import models

from account.models import User


class Genre(models.Model):
    """ Модель жанров треков
    """
    name = models.CharField(max_length=25, unique=True)
    slug = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    """ Модель треков
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, related_name='track_genres')
    audio = models.FileField(
        upload_to='audios')
    image = models.ImageField(
        upload_to='images',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    """ Модель комментариев к треку
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)






























