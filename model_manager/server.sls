{%- from "model_manager/map.jinja" import server with context %}
{%- if server.enabled %}

model_manager_packages:
  pkg.installed:
  - names: {{ server.pkgs }}

{{ server.dir.base }}:
  virtualenv.manage:
  - system_site_packages: True
  - python: /usr/bin/python
  - require:
    - pkg: model_manager_packages

{%- if server.source.commit_id is defined %}

model_manager_source:
  git.detached:
  - name: {{ server.source.address }}
  - target: {{ server.dir.base }}/source
  {%- if grains.saltversioninfo.0 > 2016 %}
  - rev: {{ server.source.commit_id }}
  {%- else %}
  - ref: {{ server.source.commit_id }}
  {%- endif %}
  - require:
    - virtualenv: {{ server.dir.base }}

{%- else %}

model_manager_source:
  git.latest:
  - name: {{ server.source.address }}
  - target: {{ server.dir.base }}/source
  - rev: HEAD
  - branch: {{ server.source.revision }}
  - require:
    - virtualenv: {{ server.dir.base }}

{%- endif %}

model_manager_requirements:
  pip.installed:
  - name: gunicorn
  - requirements: {{ server.dir.base }}/source/requirements.txt
  - bin_env: {{ server.dir.base }}/bin/pip
  - require:
    - git: model_manager_source

model_manager_user:
  user.present:
  - name: model_manager
  - system: true
  - home: {{ server.dir.base }}
  - require:
    - virtualenv: {{ server.dir.base }}

model_manager_dir:
  file.directory:
  - names:
    - {{ server.dir.base }}/site/local
    - {{ server.dir.base }}/static
    - {{ server.dir.base }}/media
    - {{ server.dir.log }}
    - /etc/model-manager
  - mode: 700
  - makedirs: true
  - user: model_manager
  - require:
    - virtualenv: {{ server.dir.base }}

model_manager_config:
  file.managed:
  - name: /etc/model-manager/settings.py
  - source: salt://model_manager/files/model_manager.settings.py
  - template: jinja
  - user: model_manager
  - mode: 600
  - require:
    - file: model_manager_dir

{% if server.config_files is defined %}

model_manager_enabled_init:
  file.managed:
  - name: {{ server.dir.base }}/source/model_manager/settings/enabled/__init__.py
  - contents: ""
  - user: model_manager
  - require:
    - git: model_manager_source
  - require_in:
    - file: model_manager_config_dir

{%- for config_file in server.get('config_files', []) %}

model_manager_enabled_{{ config_file }}:
  file.managed:
  - name: {{ server.dir.base }}/source/model_manager/settings/enabled/{{ config_file }}.py
  - source: salt://model_manager/files/config_files/{{ config_file }}.py
  - user: model_manager
  - require:
    - git: model_manager_source
  - require_in:
    - file: model_manager_config_dir

{%- endfor %}

model_manager_config_dir:
  file.directory:
  - names:
    - {{ server.dir.base }}/source/model_manager/settings/enabled
  - user: model_manager
  - clean: true
  - require:
    - git: model_manager_source

{%- endif %}

model_manager_wsgi:
  file.managed:
  - name: {{ server.dir.base }}/wsgi.py
  - source: salt://model_manager/files/model_manager.wsgi.py
  - template: jinja
  - user: model_manager
  - mode: 777
  - require:
    - file: model_manager_dir

model_manager_start_script:
  file.managed:
  - name: {{ server.dir.base }}/bin/model_manager
  - source: salt://model_manager/files/model_manager
  - template: jinja
  - user: model_manager
  - mode: 744
  - require:
    - file: model_manager_dir
    - file: model_manager_wsgi

model_manager_service_script:
  file.managed:
  - name: /etc/systemd/system/model-manager.service
  - source: salt://model_manager/files/model-manager.service
  - template: jinja
  - user: root
  - mode: 644
  - require:
    - file: model_manager_start_script

model_manager_restart_systemd:
  module.wait:
  - name: service.systemctl_reload
  - watch:
    - file: model_manager_service_script

model_manager_service:
  service.running:
  - name: model-manager
  - enable: true
  - require:
    - git: model_manager_source
  - watch:
    - file: model_manager_config
    - file: model_manager_service_script

{%- endif %}

