from django.db import models
from acc.models import User

class Book(models.Model):
    site_name = models.CharField(max_length=100)
    site_url = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    impo = models.BooleanField(default=False)
    pubdate = models.DateTimeField()

    def __str__(self):
        return f"[{self.user}] {self.site_name}"
