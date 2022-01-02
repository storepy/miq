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
coverage run -m pytest tests/auth/test_auth_image_viewset.py::TestImageViewset::test_create

coverage html
```
