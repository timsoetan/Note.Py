from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


# custom user model manager
# handles email being used for authentication
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# custom user model
# uses email for authentication instead of username
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email_address'), unique=True, null=True)
    first_name = models.TextField()
    last_name = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


# sticky note model
class StickyNote(models.Model):
    objects = models.Manager()
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='creator')
    id = models.AutoField(primary_key=True)
    left = models.TextField()
    top = models.TextField()
    z_index = models.TextField()
    time_stamp = models.TextField()
    text = models.TextField()
    rotation_style = models.TextField()
    note_color = models.TextField()
    note_border_color = models.TextField()
    pen_color = models.TextField()
