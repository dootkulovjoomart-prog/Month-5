from rest_framework import serializers
from .models import Film , Director


class DirectorSErializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio  '.split()

class FilmListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    director = DirectorSErializer(many =False)
    class Meta:
        model = Film
        fields = 'title text release_year rating is_hit created updated director genres genre_list reviews'.split()
        # depth = 1
    def get_genres(self ,film):
        return [i.name for i in film.genres.all()]

class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
