import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ROLE_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    sur_name = models.CharField(max_length=64)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'sur_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email} - registered'
    
class Result(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    finalConstructionDate = models.DateTimeField(auto_now_add=True)
    CountCompletedQuest = models.SmallIntegerField(default=1)
    reputation = models.SmallIntegerField(default=0)
    evaluationGraphConstruction = models.SmallIntegerField(default=0)
    budget = models.DecimalField(max_digits=12, decimal_places=2)                           
    office_health = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.id} - Result created'

    
class Session(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.id} - session created'
