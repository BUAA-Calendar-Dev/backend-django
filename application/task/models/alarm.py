from django.db import models


class Alarm(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)
