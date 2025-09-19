from rest_framework import generics, permissions,status
from .models import Cell
from .serializers import CellSerializer
import io, sys
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cell


class CellCreateView(generics.CreateAPIView):
    serializer_class = CellSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        file_id = self.kwargs["pk"]
        serializer.save(file_id=file_id)


class CellUpdateView(generics.UpdateAPIView): #셀 코드 수정 
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(content=self.request.data.get("content"))

class CellDeleteView(generics.DestroyAPIView):  #셀 삭제
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    permission_classes = [permissions.IsAuthenticated]

class CellRunView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            cell = Cell.objects.get(pk=pk)
        except Cell.DoesNotExist:
            return Response({"error": "Cell not found"}, status=status.HTTP_404_NOT_FOUND)

        code = cell.content
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            exec(code, {})  # exec()는 로컬 학습 용도로는 괜찮지만 운영에서는 Sandbox 필요
            output = sys.stdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout

        # 실행 결과 DB에 저장
        cell.output = output
        cell.save()

        return Response(CellSerializer(cell).data, status=status.HTTP_200_OK)