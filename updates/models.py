from django.db import models

class HealthUpdate(models.Model):
    patient_name = models.CharField(max_length=100)
    status = models.TextField()
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name