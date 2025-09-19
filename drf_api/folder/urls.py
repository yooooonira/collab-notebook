from django.urls import path
from .views import FolderListCreateView, FolderDeleteView

urlpatterns = [
    path("", FolderListCreateView.as_view(), name="folder-list-create"), #폴더 목록 조회/생성 
    path("<int:pk>/", FolderDeleteView.as_view(), name="folder-delete"), #폴더 삭제
]