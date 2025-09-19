from django.urls import path
from .views import FolderListCreateView, FolderDeleteView,FolderFileListCreateView

urlpatterns = [
    path("", FolderListCreateView.as_view(), name="folder-list-create"), #폴더 목록 조회/생성 
    path("<int:pk>/", FolderDeleteView.as_view(), name="folder-delete"), #폴더 삭제
    path("<int:pk>/files/", FolderFileListCreateView.as_view(), name="folder-delete"), #폴더기준 파일 조회/생성 

]