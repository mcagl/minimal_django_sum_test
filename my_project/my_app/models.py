from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32)


class Row(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    day = models.DateField()
    tags = models.ManyToManyField(Tag, related_name='rows')
