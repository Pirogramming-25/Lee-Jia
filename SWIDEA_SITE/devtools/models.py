from django.db import models

# Create your models here.
class DevTool(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    