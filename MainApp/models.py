from django.db import models

# Create your models here.
class PatientMessage(models.Model):
    CATEGORY_CHOICES = [
        ('emergency', 'Emergency'),
        ('routine', 'Routine'),
        ('follow-up', 'Follow-up'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20, db_index=True)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.category} ({self.confidence:.2f})"
    
    

