# The slug of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'delivery'
# If set to True, this dashboard will be set as the default dashboard.
DEFAULT = False
# A dictionary of exception classes to be added to HORIZON['exceptions'].
ADD_EXCEPTIONS = {}
# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = ['model_manager.dashboards.delivery']

AUTO_DISCOVER_STATIC_FILES = True

ADD_JS_FILES = []

ADD_JS_SPEC_FILES = []

