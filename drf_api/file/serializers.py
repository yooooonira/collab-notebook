from rest_framework import serializers
from .models import File
from cell.models import Cell  
from user.models import UserProfile

class FileSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )
    invited_students = serializers.SlugRelatedField(
        many=True,
        queryset=UserProfile.objects.all(),
        slug_field="email",
        required=False
    )

    class Meta:
        model = File
        fields = [
            "id",
            "name",
            "folder",
            "owner",
            "file_type",
            "invited_students",
        ]
        read_only_fields = ["id", "folder", "owner", "file_type"]

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ["id", "file", "content", "output"]
        read_only_fields = ["id", "file", "output"] 