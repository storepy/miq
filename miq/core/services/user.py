from typing import List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


from .permission import perm_get

User = get_user_model()


def user_add_perms(user:User, *, codenames:List[str], refresh:bool=False) -> User:
    """
    Add permissions to user.
    Codenames must be valid permission codenames in format <action>_<model> for ex: add_product.
    
    Arguments:
    user -- user[User]

    Keyword arguments:
    codenames -- codenames[List[str]]
    refresh -- refresh user[bool] (default False)
    """

    for perm in Permission.objects.filter(codename__in=codenames):
        user.user_permissions.add(perm)

    if refresh:
        user = User.objects.get(username=user.username)

    return user


def user_add_perm(user:User, *, codename:str, refresh:bool=False) -> User:
    """
    Add permission to user.
    Codename must be a valid permission codename in format <action>_<model> for ex: add_product.
    
    Arguments:
    user -- user[User]

    Keyword arguments:
    codename -- codename[str]
    refresh -- refresh user[bool] (default False)
    """

    perm: Permission = perm_get(codename)
    user.user_permissions.add(perm)

    if refresh:
        user = User.objects.get(username=user.username)

    return user


def user_create(*, username: str, email: str, password: str, first_name:str, last_name:str, **kwargs) -> User:
    """Create and return a new user.
    May raise ValidationError.


    Keyword arguments:

    username -- username[str]
    email -- email[str]
    password -- password[str]
    first_name -- first name[str]
    last_name -- last name[str]
    gender -- gender[UserGender] (default UserGender.OTHER)
    img -- profile picture[Image] (default None)
    is_staff -- is staff[bool] (default False)
    is_superuser -- is superuser[bool] (default False)
    is_active -- is active[bool] (default True)
    date_joined -- date joined[datetime] (default timezone.now())
    """

    user = User(username=username,email=email,first_name=first_name,last_name=last_name, **kwargs)
    user.set_password(password)

    user.full_clean()
    user.save()

    return user