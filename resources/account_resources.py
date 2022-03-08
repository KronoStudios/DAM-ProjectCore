#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import datetime
import logging
import os

import falcon
from falcon.media.validators import jsonschema

import messages
import settings
from db.models import User, UserToken
from hooks import requires_auth
from resources import utils
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaUserToken
from settings import STATIC_DIRECTORY

mylogger = logging.getLogger(__name__)

@falcon.before(requires_auth)
class ResourceAccountUserProfile(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceAccountUserProfile, self).on_get(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]

        resp.media = current_user.json_model
        resp.status = falcon.HTTP_200

@falcon.before(requires_auth)
class ResourceAccountUpdateProfileImage(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceAccountUpdateProfileImage, self).on_post(req, resp, *args, **kwargs)


        # Get the user from the token
        current_user = req.context["auth_user"]
        resource_path = current_user.photo_path

        # Get the file from form
        incoming_file = req.get_param("image_file")

        # Run the common part for storing
        filename = utils.save_static_media_file(incoming_file, resource_path)

        # Update db model
        current_user.photo = filename
        self.db_session.add(current_user)
        self.db_session.commit()

        resp.status = falcon.HTTP_200