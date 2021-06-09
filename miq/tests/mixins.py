from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMixin:

    username = 'usr'
    password = 'pwd'
    user = None

    def get_user(self, username=None, password=None):
        if not username and not self.user:
            self.user = self.create_user(self.username, self.password)
            return self.user

        if not username and self.user:
            return self.user

        if not username or not password:
            raise Exception('Username/password required.')

        return self.create_user(username, password)

    def create_user(self, username, password):
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        return user


class SiteMixin:
    @property
    def site(self):
        return Site.objects.first()

    def create_site(self):
        return Site.objects.create()


class TestMixin(SiteMixin, UserMixin):
    pass
