from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .models import Film
from .serializers import (
    FilmListSerializer ,
    FilmDetailSerializer ,
    FilmValidateSerializer
    )

from django.db import transaction
from rest_framework import status

@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method =='GET':
        film = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()
        data = FilmListSerializer(film , many = True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = FilmValidateSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST ,
                            data=serializer.errors)
        print(serializer.validated_data)
        

        title = serializer.validated_data.get('title')
        print(title)
        text = serializer.validated_data.get('text')
        release_year = serializer.validated_data.get('release_year')
        rating = serializer.validated_data.get('rating')
        is_hit = serializer.validated_data.get('is_hit')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        print(request.data)


        with transaction.atomic():
            film = Film.objects.create(
                title=title,
                text=text,
                rating=rating,
                release_year=release_year,
                is_hit = is_hit,
                director_id = director_id

            )

            film.genres.set(genres)
            film.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    

@api_view(['GET','PUT' , 'DELETE'])
def film_detail_api_view(request , id):
    try:
        film = Film.objects.get(id = id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film , many = False ).data
        return Response(data=data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        film.title = serializer.validated_data.get('title')
        film.text = serializer.validated_data.get('text')
        film.release_year = serializer.validated_data.data.get('relaese_year')
        film.rating = serializer.validated_data.get('rating')
        film.is_hit = serializer.validated_data.get('is_hit')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)



