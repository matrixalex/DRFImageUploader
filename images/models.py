from django.db import models


class CustomImage(models.Model):
    file = models.FileField()
    file_name = models.TextField()

    def __str__(self):
        return str(self.file)
