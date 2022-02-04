from django.urls import path
from . import views

app_name = "book"
urlpatterns = [
    path('book/', views.index, name="index"),
    path('create/', views.create, name="create"),
    
]