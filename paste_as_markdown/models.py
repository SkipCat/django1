from django.db import models

class Markdown(models.Model):
    content = models.TextField()
    alias = models.CharField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return self.content
