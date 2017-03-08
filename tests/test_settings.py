SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests", "django_rest_cryptingfields"
]

HMAC_KEY = '232lkjl2k3jlkjl2k34lkj234lkj2l3lkjeoicioo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dentalemr',
        'USER': 'me',
        'PASSWORD': 'suni!skyz',
        'HOST': 'localhost',
        'PORT': '',
    }
}

MIDDLEWARE_CLASSES = (
)


