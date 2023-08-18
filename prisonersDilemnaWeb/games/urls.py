from django.urls import path

from . import views

app_name='games'

urlpatterns = [
    path("addPlayerUpdater/", views.addPlayerUpdater, name="addPlayerUpdater"),
    path("createNewPlayer/", views.createNewPlayer, name="createNewPlayer"),
    path("playerDetail/<int:pk>", views.playerDetail.as_view(), name="playerDetail"),
]