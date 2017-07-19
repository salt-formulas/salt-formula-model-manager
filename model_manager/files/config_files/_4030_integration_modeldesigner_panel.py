# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'modeldesigner'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'integration'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'models'

# If set, it will update the default panel of the PANEL_DASHBOARD.
DEFAULT_PANEL = 'modeldesigner'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'model_manager.dashboards.integration.modeldesigner.panel.ModelDesigner'

