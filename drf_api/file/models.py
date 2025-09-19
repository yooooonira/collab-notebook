from django.db import models
from django.conf import settings
from folder.models import Folder
from user.models import UserProfile

class File(models.Model):
    FILE_TYPES = (
        ("교재용", "교재용"),
        ("학습용", "학습용"),
        ("자습용", "자습용"),
    )

    name = models.CharField(max_length=30)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="files")
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)

    # 🔹 학생 초대 (ManyToMany)
    invited_students = models.ManyToManyField(
        UserProfile, related_name="invited_files", blank=True
    )

    def __str__(self):
        return self.name
