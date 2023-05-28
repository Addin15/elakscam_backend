from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.
class Account(models.Model):
    id = None
    number = models.CharField(max_length=255, unique=True, primary_key=True)
    holder_name = models.CharField(max_length=255, null=True, blank=True)
    holder_nric = models.CharField(max_length=50, null=True, blank=True)
    evidence_score = models.IntegerField(default=0)
    appealed = models.BooleanField(default=False)

class Report(models.Model):
    def report_document_loc(self, filename):
        return "documents/reports/{id}/{filename}".format(
            id=self.id, filename=filename
        )
    account_number = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    evidence = models.FileField(upload_to=report_document_loc, null=True, blank=True)
    evidence_description = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('account_number', 'reported_by',)


