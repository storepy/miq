from django.apps import apps


def serialize_app_config(app_config):
    return {
        'label': app_config.label,
        'name': app_config.verbose_name,
        'models': [key for key in app_config.models.keys()]
    }


def get_serialized_app_configs_dict(exclude=None, exclude_django_apps=False):
    exclude = exclude if isinstance(exclude, list) else []
    if exclude_django_apps:
        exclude.extend([
            'admin', 'auth', 'contenttypes', 'messages',
            'sessions', 'sitemaps', 'sites', 'staticfiles'
        ])

    installed_apps = [
        serialize_app_config(app)
        for app in apps.get_app_configs()
    ]
    return {
        f"{app['label']}": app for app in installed_apps
        if f"{app['label']}" not in exclude
    }


def get_user_perms_list(user):
    return list(user.get_all_permissions())


def get_user_perms_dict(user):
    perms = get_user_perms_list(user)
    return {'count': len(perms), 'perms': perms}


def get_text_choices(TextChoiceModel):
    return [
        {'name': choice.name, 'label': choice.label, 'value': choice.value}
        for choice in TextChoiceModel
    ]
