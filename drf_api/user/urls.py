from django.urls import path
from . import views

urlpatterns = [
    # signup, login은 Supabase에서 처리하니까 drf에서는 필요없다. 
    path("auth/me/", views.MyInfo.as_view(), name="my-info"),
    path("users/search/", views.Search.as_view(), name="search"),
]
