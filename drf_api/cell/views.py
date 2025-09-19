from rest_framework import generics, permissions
from .models import Cell
from .serializers import CellSerializer

class CellCreateView(generics.CreateAPIView):
    serializer_class = CellSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        file_id = self.kwargs["pk"]
        serializer.save(file_id=file_id)
