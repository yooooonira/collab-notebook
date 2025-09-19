from rest_framework import generics, permissions
from .models import Folder
from .serializers import FolderSerializer

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "teacher"

class FolderListCreateView(generics.ListCreateAPIView):  #폴더 목록 조회/생성 
    serializer_class = FolderSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "teacher":
            return Folder.objects.filter(owner=user)
        elif getattr(user, "role", None) == "student":
            return Folder.objects.filter(files__invited_students=user).distinct()
        return Folder.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

class FolderDeleteView(generics.DestroyAPIView):  #폴더 삭제
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    def get_permissions(self):
        return [IsTeacher()]
