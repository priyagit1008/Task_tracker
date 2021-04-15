import uuid

from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from libs.models import TimeStampedModel


from model_utils import Choices
from django.contrib.postgres.fields import ArrayField

from django.db.models import CharField

# Create your models here.
class Task_tracker(TimeStampedModel):
    """
    User model represents the user data in the database.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 

    task_name = models.CharField(max_length=64, blank=False)
    project_name = models.CharField(max_length=64, null=True, blank=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    discription = models.CharField(max_length=64,blank=True,null=True)

    class Meta:
        app_label = 'Task_traker'
        db_table = 'api_task'

