from django.db import models
from apps.core.models import BaseModel


class Airline(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        app_label = "airlines"

    def __str__(self):
        return self.name


class Aircraft(BaseModel):
    model = models.CharField(max_length=50)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    class Meta:
        app_label = "airlines"

    def __str__(self):
        return f"{self.model} ({self.airline.code})"
