from django.urls import path
from .views import CellUpdateView, CellDeleteView, CellRunView
urlpatterns = [
    path("<int:pk>/update/", CellUpdateView.as_view(), name="cell-update"), #셀 코드 수정
    path("<int:pk>/delete/", CellDeleteView.as_view(), name="cell-delete"), #셀 삭제
    path("<int:pk>/run/", CellRunView.as_view(), name="cell-run"), #셀 실행

]
