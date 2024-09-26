from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # 这里将 related_name 改为 'custom_users'
        related_query_name='custom_user',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  # 这里将 related_name 改为 'custom_users'
        related_query_name='custom_user',
        blank=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'user'
