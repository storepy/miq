# Marqetintl Core App

## Deployment

## Running tests

- pytest

```
python -m pytest

```

- coverage

```
coverage run -m pytest

<!-- run specific test -->
coverage run -m pytest analytics/tests/test_hit.py::TestHitModel::test_create_hit

<!-- ignore a directory -->
coverage run -m pytest --ignore miq/staff

coverage html
```

install extra requires

```
pip3 install -e .\[extra\]
```

## Required template files:

- base.django.html
- public.django.html

### Base Public layout

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta content="width=device-width,initial-scale=1,maximum-scale=1,shrink-to-fit=no" name="viewport" />

    {% block head %}{% endblock head %}

    <!-- react css styles -->
    <link href="/static/css/react.css.chunks" rel="stylesheet" />

    <!-- prettier-ignore -->
    {% block css_links %}
        <link href="{% static "miq.css" %}?{% now "U" %}" rel="stylesheet">
    {% endblock css_links %}

    <style id="page-css" type="text/css">
      {% block css %}{% endblock css %}
    </style>
  </head>

  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>

    <!-- prettier-ignore -->
    {% block pre_react %}
    <div class="public">
      <header id="public-header">
        <!-- prettier-ignore -->
        {% block navbar %}{% endblock navbar %}

        {% block header %}{% endblock header %}
      </header>

      <main id="public-main" role="main">{% block main %}{% endblock main %}</main>
    </div>
    {% endblock pre_react %}

    <!-- prettier-ignore -->
    {% block react %}
    <div id="root"></div>
    {% endblock react %}

    <!-- prettier-ignore -->
    {% block post_react %}
    <footer id="public-footer">{% block footer %}{% endblock footer %}</footer>
    {% endblock post_react %}

    <script>
      //   react static files loading script
    </script>
    <script src="/static/js/react-script-chucks"></script>
  </body>
</html>
```

### Base template layout

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta content="width=device-width,initial-scale=1,maximum-scale=1,shrink-to-fit=no" name="viewport" />

    {% block head %}{% endblock head %}

    <!-- react css styles -->
    <link href="/static/css/react.css.chunks" rel="stylesheet" />

    {% block css_links %}{% endblock css_links %}

    <style id="page-css" type="text/css">
      {% block css %}{% endblock css %}
    </style>
  </head>

  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>

    <!-- prettier-ignore -->
    {% block pre_react %}{% endblock pre_react %}

    <!-- prettier-ignore -->
    {% block react %}
    <div id="root"></div>
    {% endblock react %}

    <!-- prettier-ignore -->
    {% block post_react %}{% endblock post_react %}

    <script>
      //   react static files loading script
    </script>
    <script src="/static/js/react-script-chucks"></script>
  </body>
</html>
```
