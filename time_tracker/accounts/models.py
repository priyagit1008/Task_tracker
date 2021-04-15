
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token
from libs.models import TimeStampedModel

from .managers import UserManager

from model_utils import Choices
from django.contrib.postgres.fields import ArrayField

from django.db.models import CharField

def user_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    # return 'user_%S/%s'.format(instance.id,filename)
    # extension = filename[0-5]
    return 'user_{0}/{1}.{2}'.format("images", instance.first_name, extension)



class User(TimeStampedModel):
    """
    User model represents the user data in the database.
    """
    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
    )

    GENDER = Choices(
        ('Male','MALE'),
        ('Female','FEMALE'),
        ('Other','OTHER'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 

    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    mobile = models.BigIntegerField(
        validators=[
            MinValueValidator(5000000000),
            MaxValueValidator(9999999999),
        ],
        unique=True,
        db_index=True, blank=False)
    dob = models.DateField(blank=True,null=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    pincode = models.CharField(max_length=64,blank=True,null=True)
    qualification = models.CharField(max_length=64,null=True, blank=True)
    status = models.CharField(max_length=64, choices=STATUS, blank=True, default=STATUS.active)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    class Meta:
        app_label = 'accounts'
        db_table = 'api_user'

    def __str__(self):
        return str(self.mobile)

    @property
    def access_token(self):
        token, is_created = Token.objects.get_or_create(user=self)
        return token.key
