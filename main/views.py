from rest_framework.generics import ListCreateAPIView

from main.models import Song, Singer, Album
from main.serializers import SongListSerializer, SongSerializer, SingerListSerializer, SingerSerializer, \
    AlbumListSerializer, AlbumSerializer


class ListCreateSingerView(ListCreateAPIView):
    queryset = Singer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SingerListSerializer
        return SingerSerializer


class ListCreateAlbumView(ListCreateAPIView):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AlbumListSerializer
        return AlbumSerializer


class ListCreateSongView(ListCreateAPIView):
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SongListSerializer
        return SongSerializer


