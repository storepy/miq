import pytest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from miq.tests.utils import get_random_user_data
from miq.core.services.user import user_create, user_add_perm, user_add_perms


User = get_user_model()


@pytest.mark.django_db
def test_user_add_perms():
    user = user_create(**get_random_user_data())

    assert user.has_perm('core.add_image') is False

    user = user_add_perms(user, codenames=['add_image', 'change_image', 'delete_image'], refresh=True)
    assert user.has_perm('core.add_image') is True
    assert user.has_perm('core.change_image') is True
    assert user.has_perm('core.delete_image') is True


@pytest.mark.django_db
def test_user_add_perm():
    user = user_create(**get_random_user_data())

    assert user.has_perm('core.add_image') is False
    
    user = user_add_perm(user, codename='add_image')

    # User refresh is required by django internals
    assert user.has_perm('core.add_image') is False
    assert User.objects.get(username=user.username).has_perm('core.add_image') is True

    assert user.has_perm('core.change_image') is False
    user = user_add_perm(user, codename='change_image', refresh=True)
    assert user.has_perm('core.change_image') is True


@pytest.mark.django_db
def test_user_create():

    data = {
        "first_name": "",
        "last_name": "",
        "username": "testuser",
        "email": "email",
        "password": "pwd"
    }

    with pytest.raises(ValidationError):
        user_create(**data)
    
    data.update({
        "first_name": "fname",
        "last_name": "lname",
    })

    with pytest.raises(ValidationError):
        user_create(**data)

    data['email'] = "testuser@email.email"

    user = user_create(**data)
    assert f'{user}' == data['username']
    assert user.username == data['username']
    assert user.email == data['email']
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']
    assert user.check_password(data['password']) is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_active is True


    
    
