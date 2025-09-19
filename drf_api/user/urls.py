from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignupView.as_view(), name="signup"),
    path("auth/me/", views.MyInfo.as_view(), name="my-info"),
    path("users/search/", views.Search.as_view(), name="search"),
    path("users/available/", views.AvailableUserList.as_view(), name="user-available"), #권한부여용 이용자 목록 조회 
]
  