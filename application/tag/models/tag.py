from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=1024, default="tag名", verbose_name="tag_name")

    def __str__(self):
        return f"{self.name} {self.id}"

    class Meta:
        db_table = 'tag'
