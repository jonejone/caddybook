
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'sorl.thumbnail',
    'geoposition',

    'caddybook.books',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/jone/git-repos/caddybook/_db.db',
    }
}

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
ROOT_URLCONF = 'caddybook.books.urls'
#LANGUAGE_CODE = 'nb_NO'

STATICFILES_DIRS = ('/home/jone/caddybook/static', '/home/jone/caddybook/caddybook/books/static')
#LOCALE_PATHS = ('/home/jone/git-repos/clubmembers/conf/locale',)

MEDIA_ROOT = '/home/jone/git-repos/caddybook/media'
MEDIA_URL = '/media/'
