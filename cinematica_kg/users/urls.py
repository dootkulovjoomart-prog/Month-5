from django.urls import path
from . import views

urlpatterns = [
    path('registration/' , views.registration_api_view),
    path('autorization/' , views.authorization_api_view)
   
]