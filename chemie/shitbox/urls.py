from django.urls import path
from . import views

app_name = "shitbox"

urlpatterns = [
    path("liste/", submissions_overview, name="list"),
    path("api/", views.ListAllShitbox.as_view()),
    path("api/<int:pk>/", views.ShitboxDetail.as_view()),
    path("", post_votes, name="index"),
    path("toggle-used", toggle_used, name="toggle-used"),
]
