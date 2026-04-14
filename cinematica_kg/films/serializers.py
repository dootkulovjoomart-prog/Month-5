from rest_framework import serializers
from .models import Film , Director , Genre
from rest_framework.exceptions import  ValidationError


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


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required = True , min_length = 2 , max_length = 255)
    text = serializers.CharField()
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value = 1 ,max_value = 10)
    is_hit = serializers.BooleanField(default = True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child = serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exixt')
        return director_id
    
    def validate_genres(self , genres):
        genres = list(set(genres))
        genres1 = Genre.objects.filter(id__in = genres)
        if len(genres1) != len(genres):
            raise ValidationError('Genres does not exixt')
        return genres


