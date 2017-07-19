{%- from "model_manager/map.jinja" import server with context %}

SECRET_KEY = '{{ server.secret }}'
DEBUG = True

AVAILABLE_THEMES = [
    ('vendor', 'Default', 'themes/vendor')
]

DEFAULT_THEME = "vendor"

TEMPLATE_LOADERS = (
    'model_manager.utils.themes.ThemeTemplateLoader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader',
)

{%- if server.integration is defined %}
JENKINS_API_URL = "localhost"
JENKINS_API_USERNAME = "username"
JENKINS_API_PASSWORD = "password"
{%- endif %}

COOKIECUTTER_JENKINS_JOB = "cookiecutter-job"
COOKIECUTTER_CONTEXT_REMOTE = "http"
COOKIECUTTER_CONTEXT_URL = "https://git.my-gitlab.io/group/project/raw/master/context.yaml"

SALT_API_URL="http://172.16.1.200:6969"
SALT_API_USER="manager"
SALT_API_PASSWORD="password"
SALT_API_EAUTH="pam"
SALT_API_POLLING_INTERVAL=5

{%- if server.identity.engine == 'keystone' %}

OPENSTACK_API_VERSIONS = {
    'identity': 3
}
OPENSTACK_HOST = 'vpc.tcpisek.cz'
OPENSTACK_KEYSTONE_URL = 'https://%s:5000/v3' % OPENSTACK_HOST
OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'Member'

AUTHENTICATION_URLS = ['openstack_auth.urls']
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
AUTH_USER_MODEL = 'openstack_auth.User'

INSTALLED_APPS = [
    'model_manager',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_pyscss',
    'model_manager.django_pyscss_fix',
    'compressor',
    'horizon',
    'openstack_auth'
]

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
