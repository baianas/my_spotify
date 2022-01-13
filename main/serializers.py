from rest_framework import serializers

from main.models import Feat, Song, Genre, Singer, Album


class SingerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = ['id', 'name', 'image']


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'


class FeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feat
        fields = '__all__'


class AlbumListSerializer(serializers.ModelSerializer):
    feats = FeatSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'singer', 'feats', 'image', 'pal']


class AlbumSerializer(serializers.ModelSerializer):
    feats = FeatSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'


class SongListSerializer(serializers.ModelSerializer):
    feats = FeatSerializer(many=True)

    class Meta:
        model = Song
        fields = ['id', 'name', 'singer', 'image']


class SongSerializer(serializers.ModelSerializer):
    feats = FeatSerializer

    class Meta:
        model = Song
        exclude = ('album', 'uploaded_at', 'pal', 'genre')


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['slug', 'name', 'image']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'



