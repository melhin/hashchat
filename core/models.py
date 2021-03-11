import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.managers import UserManager
from core.choices import AuthentiationMethod, LanguageChoices


class AbstractBase(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, AbstractBase):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    auth_method = models.CharField(
        max_length=40,
        choices=[(auth, auth.value) for auth in AuthentiationMethod]
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfile(AbstractBase):
    user = models.OneToOneField('core.User', related_name='profile', on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)
    company = models.CharField(max_length=50)
    language_code = models.CharField(
        max_length=3,
        choices=[(lang, lang.value) for lang in LanguageChoices],
        default=LanguageChoices.EN.value,
    )