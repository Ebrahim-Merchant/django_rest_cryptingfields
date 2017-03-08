import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django_rest_cryptingfields",
    version = "0.0.1",
    author = "Russell Morley",
    author_email = "russ@compass-point.net",
    description = ("A rest_framework serializer field that encrypts text upon deserialization and decrypts upon serialization."),
    license = "MIT",
    keywords = "rest framework django encryption serializer fields",
    url = "https://github.com/russellmorley/django_rest_cryptingfields",
    packages=['django_rest_cryptingfields'],
    install_requires=['python-keyczar==0.715', 'django>=1.8.14', 'djangorestframework>=3.4.1'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
)



