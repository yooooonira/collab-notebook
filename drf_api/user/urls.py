from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignupView.as_view(), name="signup"),
    path("auth/me/", views.MyInfo.as_view(), name="my-info"),
    path("users/search/", views.Search.as_view(), name="search"),
]
  