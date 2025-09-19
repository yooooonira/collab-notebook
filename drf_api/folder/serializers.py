from rest_framework import serializers
from .models import Folder
from file.models import File
from user.models import UserProfile

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "owner"]
        read_only_fields = ["id", "owner"]



class FileSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )
    # 🔹 invited_students를 이메일 기반으로 주고받기
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
        read_only_fields = ["id", "owner", "folder"]