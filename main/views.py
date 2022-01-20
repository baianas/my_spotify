from rest_framework import viewsets, parsers, views
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers
from .models import Track, Comment
from .permissions import IsAuthor
from .serializers import TrackListSerializer, TrackSerializer, CommentSerializer, GenreSerializer


class ListCreateTrackView(ListCreateAPIView):
    queryset = Track.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TrackListSerializer
        return TrackSerializer


class RetrieveUpdateDeleteTrackView(RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'genre__name']

    def get_serializer_class(self):
        if self.action == 'list':
            return TrackListSerializer
        return TrackSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action == 'reviews':
            if self.request.method == 'POST':
                return [IsAuthenticated()]
            return []
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=201)

    @action(['GET', 'POST'], detail=True)
    def cooments(self, request, pk=None):
        track = self.get_object()
        if request.method == 'GET':
            comments = track.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        data = request.data
        serializer = CommentSerializer(data=data,
                                       context={'request': request,
                                                'track': track})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class GenreViewSet(ModelViewSet):
    """ Список жанров
    """
    queryset = models.Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action is ['list', 'retrieve']:
            return []
        return [IsAdminUser()]


class CreateComment(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class UpdateDeleteView(UpdateModelMixin,
                       DestroyModelMixin,
                       GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentView(viewsets.ModelViewSet):
    """ Комментарии к треку
    """
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track_id=self.kwargs.get('pk'))








