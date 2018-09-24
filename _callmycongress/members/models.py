from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=80)
    party = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
