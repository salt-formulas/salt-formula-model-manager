{%- from "model_manager/map.jinja" import server with context -%}

SECRET_KEY = '{{ server.secret_key }}'
DEBUG = {{ server.get("debug", False) }}

ALLOWED_HOSTS = ['*']

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

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

{%- if server.integration is defined %}

{%- if server.integration.engine == 'jenkins' %}

JENKINS_API_URL = '{{ server.integration.protocol }}://{{ server.integration.host }}:{{ server.integration.port }}'
JENKINS_API_USERNAME = '{{ server.integration.user }}'
JENKINS_API_PASSWORD = '{{ server.integration.password }}'

{%- endif %}

{%- if server.integration.model_template is defined %}

COOKIECUTTER_JENKINS_JOB = '{{ server.integration.model_template.job }}'
COOKIECUTTER_CONTEXT_REMOTE = '{{ server.integration.model_template.remote }}'

{# HTTP remote options #}
{%- if server.integration.model_template.remote == 'http' %}

COOKIECUTTER_CONTEXT_URL = '{{ server.integration.model_template.url }}'

{%- endif %}

{# Local filesystem remote options #}
{%- if server.integration.model_template.remote == 'localfs' %}

COOKIECUTTER_CONTEXT_PATH = '{{ server.integration.model_template.path }}'

{%- endif %}

{# Gerrit remote options #}
{%- if server.integration.model_template.remote == 'gerrit' %}

COOKIECUTTER_CONTEXT_URL = '{{ server.integration.model_template.url }}'
COOKIECUTTER_CONTEXT_PROJECT_NAME = '{{ server.integration.model_template.project_name }}'
COOKIECUTTER_CONTEXT_FILE_NAME = '{{ server.integration.model_template.file_name }}'
{%- if server.integration.model_template.username is defined and server.integration.model_template.username %}
COOKIECUTTER_CONTEXT_USERNAME = '{{ server.integration.model_template.username }}'
{%- endif %}
{%- if server.integration.model_template.password is defined and server.integration.model_template.password %}
COOKIECUTTER_CONTEXT_PASSWORD = '{{ server.integration.model_template.password }}'
{%- endif %}

{%- endif %}

{# Versioning - only supported with Gerrit remote #}
{%- if server.integration.model_template.get('versioning', {}).get('enabled', False) %}

COOKIECUTTER_CONTEXT_VERSIONING_ENABLED = True
COOKIECUTTER_CONTEXT_VERSION_FILTER = '{{ server.integration.model_template.versioning.get("filter", "") }}'
COOKIECUTTER_CONTEXT_VERSION_MAP = {{ server.integration.model_template.versioning.get('map', {}) }}

{%- endif %}

{%- endif %}

{%- endif %}

{%- if server.delivery is defined %}

{%- if server.delivery.engine == 'salt' %}

SALT_API_URL = '{{ server.delivery.protocol }}://{{ server.delivery.host }}:{{ server.delivery.port }}'
SALT_API_USER = '{{ server.delivery.user }}'
SALT_API_PASSWORD = '{{ server.delivery.password }}'
SALT_API_EAUTH = 'pam'
SALT_API_POLLING_INTERVAL = 5

{%- endif %}

{%- endif %}

{%- if server.identity.engine == 'keystone' %}

OPENSTACK_API_VERSIONS = {
    'identity': {{ server.identity.get('api_version') }},
}

OPENSTACK_HOST = "{{ server.identity.host }}"
OPENSTACK_ENDPOINT_TYPE = "{{ server.identity.get('endpoint', 'publicURL') }}"
{%- if server.identity.get('api_version') == 3 %}
OPENSTACK_KEYSTONE_URL = '{{ server.identity.protocol }}://%s:5000/v3' % OPENSTACK_HOST
{%- else %}
OPENSTACK_KEYSTONE_URL = '{{ server.identity.protocol }}://%s:5000/v2.0' % OPENSTACK_HOST
{%- endif %}
OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'Member'

AUTHENTICATION_URLS = ['openstack_auth.urls']
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
AUTH_USER_MODEL = 'openstack_auth.User'

{%- endif %}

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '{{ server.dir.log }}/model-manager.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'model_manager': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
