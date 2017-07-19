# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'resource_topology'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'delivery'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'resource_management'

# If set, it will update the default panel of the PANEL_DASHBOARD.
DEFAULT_PANEL = 'resource_topology'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'model_manager.dashboards.delivery.resource_topology.panel.ResourceTopology'
