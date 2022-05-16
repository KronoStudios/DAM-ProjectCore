#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging.config

import falcon
import pathlib

import messages
import middlewares
from falcon_multipart.middleware import MultipartMiddleware
#from resources import account_resources, common_resources, user_resources, event_resources
from resources import account_resources, user_resources, build_resources, card_resources, game_resources, common_resources, session_resources
from settings import configure_logging
from falcon_swagger_ui import register_swaggerui_app

# LOGGING
mylogger = logging.getLogger(__name__)
configure_logging()


# DEFAULT 404
# noinspection PyUnusedLocal
def handle_404(req, resp):
    resp.media = messages.resource_not_found
    resp.status = falcon.HTTP_404


# FALCON
application = app = falcon.API(
    middleware=[
        middlewares.DBSessionManager(),
        middlewares.Falconi18n(),
        MultipartMiddleware()
    ]
)

# application.add_sink(handle_404, "")

SWAGGERUI_URL = '/ui'  # without trailing slash
SCHEMA_URL = '/static/swagger.json'
STATIC_PATH = pathlib.Path(__file__).parent / 'static'

application.add_static_route('/static', str(STATIC_PATH))

application.add_route("/", common_resources.ResourceHome())

application.add_route("/cards", card_resources.Get())
application.add_route("/cards/{card}", card_resources.Find())

application.add_route("/games", game_resources.Get())
application.add_route("/games", game_resources.ResourceRegisterGame())
#application.add_route("/games/{user}", game_resources.Find())


application.add_route("/builds/{build}", build_resources.Find())
application.add_route("/builds", build_resources.Create())


application.add_route("/users", user_resources.ResourceRegisterUser())

# Auth routes
application.add_route("/session", session_resources.Create());
application.add_route("/session/delete", session_resources.Delete());


register_swaggerui_app(
    application, SWAGGERUI_URL, SCHEMA_URL,
    page_title='UI',
    favicon_url='https://falconframework.org/favicon-32x32.png',
    config={'supportedSubmitMethods': ['get'], }
)



application.add_route("/account/profile", account_resources.ResourceAccountUserProfile())
application.add_route("/account/profile/update_profile_image", account_resources.ResourceAccountUpdateProfileImage())
application.add_route("/account/create_token", account_resources.ResourceCreateUserToken())
application.add_route("/account/delete_token", account_resources.ResourceDeleteUserToken())

application.add_route("/users/register", user_resources.ResourceRegisterUser())
application.add_route("/users/show/{username}", user_resources.ResourceGetUserProfile())
'''
application.add_route("/events", event_resources.ResourceGetEvents())
application.add_route("/events/show/{id:int}", event_resources.ResourceGetEvent())
'''
application.add_sink(handle_404, "")
