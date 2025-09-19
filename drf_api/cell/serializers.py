from rest_framework import serializers
from .models import Cell

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ["id", "file", "content", "output"]
        read_only_fields = ["id", "file", "output"]  # output은 나중에 실행 결과 저장용
