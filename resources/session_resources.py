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
from db.models import User, Token
from hooks import requires_auth
from resources import utils
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaToken
from settings import STATIC_DIRECTORY

mylogger = logging.getLogger(__name__)


class Create(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super(Create, self).on_post(req, resp, *args, **kwargs)

        basic_auth_raw = req.get_header("Authorization")
        if basic_auth_raw is not None:
            basic_auth = basic_auth_raw.split()[1]
            auth_username, auth_password = (base64.b64decode(basic_auth).decode("utf-8").split(":"))
            if (auth_username is None) or (auth_password is None) or (auth_username == "") or (auth_password == ""):
                raise falcon.HTTPUnauthorized(description=messages.username_and_password_required)
        else:
            raise falcon.HTTPUnauthorized(description=messages.authorization_header_required)

        current_user = self.db_session.query(User).filter(User.email == auth_username).one_or_none()
        if current_user is None:
            current_user = self.db_session.query(User).filter(User.username == auth_username).one_or_none()

        if (current_user is not None) and (current_user.check_password(auth_password)):
            current_token = current_user.create_token()
            try:
                self.db_session.commit()
                resp.media = {"token": current_token.token}
                resp.status = falcon.HTTP_200
            except Exception as e:
                mylogger.critical("{}:{}".format(messages.error_saving_user_token, e))
                self.db_session.rollback()
                raise falcon.HTTPInternalServerError()
        else:
            raise falcon.HTTPUnauthorized(description=messages.user_not_found)

@falcon.before(requires_auth)
class Delete(DAMCoreResource):
    @jsonschema.validate(SchemaToken)
    def on_post(self, req, resp, *args, **kwargs):
        super(Delete, self).on_post(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]
        selected_token_string = req.media["token"]
        selected_token = self.db_session.query(Token).filter(Token.token == selected_token_string).one_or_none()

        if selected_token is not None:
            if selected_token.user.id == current_user.id:
                try:
                    self.db_session.delete(selected_token)
                    self.db_session.commit()

                    resp.status = falcon.HTTP_200
                except Exception as e:
                    mylogger.critical("{}:{}".format(messages.error_removing_user_token, e))
                    raise falcon.HTTPInternalServerError()
            else:
                raise falcon.HTTPUnauthorized(description=messages.token_doesnt_belongs_current_user)
        else:
            raise falcon.HTTPUnauthorized(description=messages.token_not_found)
