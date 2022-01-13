from django.db import models


class AbstractClass(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Genre(AbstractClass):
    slug = models.CharField(primary_key=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='genres')


class Singer(AbstractClass):
    bio = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='singers')


class Album(AbstractClass):
    image = models.ImageField(upload_to='albums', blank=True, null=True)
    singer = models.ForeignKey(Singer,
                               on_delete=models.CASCADE,
                               related_name='albums')
    pal = models.BooleanField(default=False)


class Song(AbstractClass):
    singer = models.ForeignKey(Album.singer,
                               on_delete=models.CASCADE,
                               related_name='songs')
    image = models.ForeignKey(Genre.image,
                              on_delete=models.CASCADE,
                              related_name='images')
    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              related_name='songs')
    uploaded_at = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)
    pal = models.ForeignKey(Album.pal,
                            on_delete=models.CASCADE,
                            related_name='pal')
    genre = models.ManyToManyField(Genre)


class Feat(models.Model):
    feat = models.ForeignKey(Singer,
                             on_delete=models.CASCADE,
                             related_name='feats')
    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              related_name='feats')
    song = models.ForeignKey(Song,
                             on_delete=models.CASCADE,
                             related_name='feats')
