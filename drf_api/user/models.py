from django.db import models

class UserProfile(models.Model):
    supabase_id = models.UUIDField(unique=True)  # Supabase가 발급해주는 UUID
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, default="student") # student/teacher
    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_authenticated(self):
        return True