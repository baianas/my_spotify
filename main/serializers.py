from rest_framework import serializers
from .models import Track, Genre, Comment


class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'user', 'title', 'audio', 'image']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug', 'name')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'create_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        track = self.context.get('track')
        validated_data['user'] = user
        validated_data['track'] = track
        return super().create(validated_data)






