from django.urls import path
from . import views

urlpatterns = [
    path("incident/", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create-incident/", views.create_incident, name="create_incident"),
    path("incident_list/", views.incident_list, name="incident_list"),
    path("incident/<str:incident_id>/edit/", views.edit_incident, name="edit_incident"),
    path("search/", views.search_incident, name="search_incident"),
]
