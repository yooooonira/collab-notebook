from rest_framework import generics, permissions
from .models import File
from .serializers import FileSerializer,CellSerializer

class FileDetailView(generics.RetrieveAPIView): #파일 열기 (파일에 속한 셀이 나옴) 
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]


class FileUpdateView(generics.UpdateAPIView): #파일 수정 (파일명 수정 ) name
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(name=self.request.data.get("name"))

class FileDeleteView(generics.DestroyAPIView):  #파일 삭제
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]


