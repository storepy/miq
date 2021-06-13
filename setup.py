from os import path
from setuptools import setup, find_packages


import miq

here = path.abspath(path.dirname(__file__))

setup(
    name='miq',
    version='1.0.0',
    description='',
    long_description='',
    url='http://github.com/marqetintl/miq',
    author='marqetintl',
    author_email='michaelgainyo@gmail.com',
    keywords='',
    license='',
    packages=find_packages(),
    install_requires=[
        "django>=2.2", 'djangorestframework', 'Pillow'
    ],
    python_requires=">=3.5",
    # test_suite='nose.collector',
    # tests_require=['nose'],
    # include_package_data=True
    zip_safe=False
)
