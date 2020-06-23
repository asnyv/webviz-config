#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AUTOMATICALLY MADE FILE. DO NOT EDIT.
# This file was generated by asny on 2020-06-22.

import logging
import logging.config
import threading
import datetime
import os.path as path
from pathlib import Path, PosixPath, WindowsPath

import dash
import dash_core_components as dcc
import dash_html_components as html
from flask_talisman import Talisman
import webviz_config
import webviz_config.certificate
from webviz_config.themes import installed_themes
from webviz_config.common_cache import CACHE
from webviz_config.webviz_store import WEBVIZ_STORAGE
from webviz_config.webviz_assets import WEBVIZ_ASSETS

import webviz_config.plugins as standard_plugins


# We do not want to show INFO regarding werkzeug routing as that is too verbose,
# however we want other log handlers (typically coming from webviz plugin dependencies)
# to be set to user specified log level.
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)

theme = webviz_config.WebvizConfigTheme("equinor")
theme.from_json((Path(__file__).resolve().parent / "theme_settings.json").read_text())

app = dash.Dash(__name__, external_stylesheets=theme.external_stylesheets)
server = app.server

app.title = "Reek Webviz Demonstration"
#app.config.suppress_callback_exceptions = True

app.webviz_settings = {
    "shared_settings": webviz_config.SHARED_SETTINGS_SUBSCRIPTIONS.transformed_settings(
        {}, PosixPath('/private/asny/webviz-config/examples'), True
    ),
    "portable": True,
    "theme": theme,
}

CACHE.init_app(server)

Talisman(server, content_security_policy=theme.csp, feature_policy=theme.feature_policy)

WEBVIZ_STORAGE.use_storage = True
WEBVIZ_STORAGE.storage_folder = path.join(
    path.dirname(path.realpath(__file__)), "webviz_storage"
)

WEBVIZ_ASSETS.portable = True

if False and not webviz_config.is_reload_process():
    # When Dash/Flask is started on localhost with hot module reload activated,
    # we do not want the main process to call expensive component functions in
    # the layout tree, as the layout tree used on initialization will anyway be called
    # from the child/restart/reload process.
    app.layout = html.Div()
else:
    app.layout = dcc.Tabs(
        parent_className="layoutWrapper",
        content_className="pageWrapper",
        vertical=True,
        children=[
          
            dcc.Tab(id="logo",
                className="styledLogo",children=[
                  standard_plugins.TablePlotter(app=app, **{'csv_file': PosixPath('/private/asny/webviz-config/examples/example_data.csv'), 'filter_cols': ['Well', 'Segment', 'Average permeability (D)'], 'plot_options': {'type': 'parallel_coordinates', 'facet_col': 'Well', 'color': 'Segment', 'barmode': 'group'}, 'filter_defaults': {'Well': ['A-1H', 'A-2H', 'C-1H']}, 'column_color_discrete_maps': {'Segment': {'A': '#ff0000', 'B': 'rgb(0,255,0)', 'C': 'blue'}}}).plugin_layout(contact_person={'name': 'Ola Nordmann', 'phone': '+47 12345678', 'email': 'some@email.com'})
                  ],
            )],
    )



if __name__ == "__main__":
    # This part is ignored when the webviz app is started
    # using Docker container and uwsgi (e.g. when hosted on Azure).
    #
    # It is used only when directly running this script with Python,
    # which will then initialize a localhost server.

    port = webviz_config.utils.get_available_port()

    token = webviz_config.LocalhostToken(app.server, port).one_time_token
    webviz_config.utils.LocalhostOpenBrowser(port, token)

    webviz_config.utils.silence_flask_startup()

    app.run_server(
        host="localhost",
        port=port,
        ssl_context=webviz_config.certificate.LocalhostCertificate().ssl_context,
        debug=True,
        use_reloader=False,
      
    )