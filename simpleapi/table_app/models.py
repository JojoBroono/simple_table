from django.db import models


class TableRow(models.Model):
    dt = models.DateField()
    name = models.CharField(max_length=1000)
    amount = models.IntegerField()
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.dt}, {self.name}, {self.amount}, {self.distance}"
