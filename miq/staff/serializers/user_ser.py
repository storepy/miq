
from django.contrib.auth import get_user_model

from miq.auth import AccountSerializer

User = get_user_model()


class StaffUserSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        fields = (
            'is_staff',
            'username', 'slug', 'email',
            'first_name', 'last_name', 'name',
            'initials', 'gender', 'gender_label',
            'img', 'img_data',
        )
