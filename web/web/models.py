# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    posted_at = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    posted_at_datetime = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.TextField(blank=True, null=True)
    sended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "jobs"
