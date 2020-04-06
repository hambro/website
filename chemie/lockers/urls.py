from django.urls import path, re_path

from . import views

app_name = "lockers"

urlpatterns = [
    path("", views.view_lockers, name="index"),
    path("<int:page>/", views.view_lockers, name="index"),
    path("registrer/<int:number>/", views.register_locker, name="registrer"),
    re_path(
        r"^aktiver/(?P<code>[a-z0-9]{32})/?",
        views.activate_ownership,
        name="activate",
    ),
    path(
        "administrer/slett/<int:locker_number>/",
        views.clear_locker,
        name="force-remove",
    ),
    path("administrer/", views.manage_lockers, name="administrate"),
    re_path(
        r"^administrer/#(?P<anchor>[-_\w]+)$",
        views.manage_lockers,
        name="administrate",
    ),
    path("mine-skap/", views.my_lockers, name="mineskap"),
]
