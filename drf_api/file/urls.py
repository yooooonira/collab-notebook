from django.urls import path
from .views import FileDetailView, FileUpdateView, FileDeleteView
from cell.views import CellCreateView
urlpatterns = [
    path("<int:pk>/", FileDetailView.as_view(), name="file-detail"),  #파일 열기 (파일에 속한 셀이 나옴) 
    path("<int:pk>/update/", FileUpdateView.as_view(), name="file-update"), #파일 수정 (파일명 수정 ) name
    path("<int:pk>/delete/", FileDeleteView.as_view(), name="file-delete"), #파일 삭제
    path("<int:pk>/cells/", CellCreateView.as_view(), name="cell-create"), #파일에 속한 셀 생성 
]