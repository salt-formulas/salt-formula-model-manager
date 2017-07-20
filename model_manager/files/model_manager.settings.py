{%- from "model_manager/map.jinja" import server with context -%}

SECRET_KEY = '{{ server.secret_key }}'
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

{%- if server.integration.engine == 'jenkins' %}

JENKINS_API_URL = '{{ server.integration.protocol }}://{{ server.integration.host }}:{{ server.integration.port }}'
JENKINS_API_USERNAME = '{{ server.integration.user }}'
JENKINS_API_PASSWORD = '{{ server.integration.password }}'

{%- endif %}

{%- if server.integration.model_template is defined %}

COOKIECUTTER_JENKINS_JOB = '{{ server.integration.model_template.job }}'
COOKIECUTTER_CONTEXT_REMOTE = '{{ server.integration.model_template.remote }}'
COOKIECUTTER_CONTEXT_URL = '{{ server.integration.model_template.url }}'

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
{%- if server.identity.get('api_version') == 3 %}
OPENSTACK_KEYSTONE_URL = '{{ server.identity.protocol }}://%s:5000/v3' % OPENSTACK_HOST
{%- else %}
OPENSTACK_KEYSTONE_URL = '{{ server.identity.protocol }}://%s:5000/v2.0' % OPENSTACK_HOST
{%- endif %}
OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'Member'

AUTHENTICATION_URLS = ['openstack_auth.urls']
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
AUTH_USER_MODEL = 'openstack_auth.User'

{% endif %}

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
