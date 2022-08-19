from os import path
from setuptools import setup, find_packages


import miq

here = path.abspath(path.dirname(__file__))

setup(
    name='miq',
    version=miq.__version__,
    description='',
    long_description='',
    url='http://github.com/marqetintl/miq',
    author='marqetintl',
    author_email=miq.__email__,
    keywords='',
    license='',
    packages=find_packages(),
    install_requires=[
        "django>=4.0.2", 'djangorestframework', 'django-environ',
        'gunicorn', 'psycopg2-binary',
        'requests', 'Pillow', 'beautifulsoup4',
        # required by analytics
        'pyyaml', 'ua-parser', 'user-agents'
    ],
    extras_require={
        "dev": [
            'coverage', 'flake8', 'autopep8', 'selenium',
            'pytest', 'pytest-cov', 'pytest-django',
        ]
    },
    python_requires=">=3.5",
    # test_suite='nose.collector',
    # tests_require=['nose'],
    # include_package_data=True
    zip_safe=False
)
