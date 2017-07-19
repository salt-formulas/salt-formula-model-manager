{%- if pillar.model_manager is defined %}
include:
{%- if pillar.model_manager.server is defined %}
- model_manager.server
{%- endif %}
{%- endif %}
