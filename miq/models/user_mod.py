from django.db import models
from django.db.models.functions import Concat
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as DjUserManager

from .mixins import BaseModelMixin


class UserQuerySet(models.QuerySet):
    def search(self, q: str, **kwargs):
        # https://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list

        if not isinstance(q, str):
            return self

        q = q.lower()
        keys = ('username', 'first_name', 'last_name', 'email')

        return self.annotate(
            values=Concat(*keys, output_field=models.CharField())
        ).filter(values__icontains=q).distinct()

    def with_perm(self, codename):
        return self.filter(
            models.Q(is_superuser=True) |
            models.Q(user_permissions__codename=codename) |
            models.Q(groups__permissions__codename=codename)
        ).distinct()

    def staff(self):
        return self.filter(is_staff=True)


class UserManager(DjUserManager):
    def staff(self):
        return self.get_queryset().staff()

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)


class UserGender(models.TextChoices):
    MALE = 'MALE', _('Male')
    FEMALE = 'FEMALE', _('Female')
    OTHER = 'OTHER', _('Other')


class User(BaseModelMixin, AbstractUser):

    REQUIRED_FIELDS = ['email', 'first_name']  # Terminal only

    # overrides
    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits '
            'and ./_ only.'),
        validators=[MinLengthValidator(
            4,
            message=_('This username is too short. (4 characters minimum)'))],
        error_messages={
            'unique': _("This username is taken."),
            'min_length': _(
                'This username is too short. (4 characters minimum)'),
        },
    )
    first_name = models.CharField(
        _('First name'), max_length=100,
        validators=[
            MinLengthValidator(2, message=_('Enter your first name.'))
        ])
    last_name = models.CharField(
        _('Last name'), max_length=100,
        validators=[MinLengthValidator(2, message=_('Enter your last name.'))])
    gender = models.CharField(
        _("Gender"), choices=UserGender.choices,
        default=UserGender.OTHER, max_length=50)

    img = models.OneToOneField(
        'miq.Image',
        verbose_name=_('Profile picture'),
        related_name='profile_pic',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.username}'

    @property
    def gender_label(self):
        return UserGender[self.gender].label

    @property
    def initials(self):
        i = ''
        if self.first_name:
            i += self.first_name[0]
        if self.last_name:
            i += self.last_name[0]

        return i.upper()
