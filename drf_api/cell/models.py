from django.db import models
from file.models import File

class Cell(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="cells")
    content = models.TextField()  # 입력 코드/내용
    output = models.TextField(null=True, blank=True)  # 실행 결과 저장

    def __str__(self):
        return f"Cell {self.id} in File {self.file.name}"
