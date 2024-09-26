from django.db import models


class Tag:
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tag'
