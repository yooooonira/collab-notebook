from rest_framework import generics, permissions
from .models import Folder
from .serializers import FolderSerializer,FileSerializer
from rest_framework.exceptions import PermissionDenied
from file.models import File

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


class FolderFileListCreateView(generics.ListCreateAPIView):  #폴더기준 파일 조회/생성 
    serializer_class = FolderSerializer
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        folder_id = self.kwargs["pk"]
        return File.objects.filter(folder_id=folder_id)

    def perform_create(self, serializer):
        folder_id = self.kwargs["pk"]
        role = self.request.user.role

        file_type = self.request.data.get("file_type")
        if role == "teacher" and file_type not in ["교재용", "학습용"]:
            raise PermissionDenied("선생은 '교재용' 또는 '학습용' 파일만 생성할 수 있습니다.")
        elif role == "student" and file_type != "자습용":
            raise PermissionDenied("학생은 '자습용' 파일만 생성할 수 있습니다.")

        serializer.save(
            folder_id=folder_id,
            owner=self.request.user
        )