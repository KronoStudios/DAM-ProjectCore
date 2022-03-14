#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from db.models import Build, Card

import falcon
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

import messages
from resources.base_resources import DAMCoreResource

mylogger = logging.getLogger(__name__)

class Find(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Find, self).on_get(req, resp, *args, **kwargs)

        build = self.db_session.query(Build).filter(Build.id == kwargs["build"]).one_or_none()

        if build is None:
            resp.status = falcon.HTTP_404
        else:
            resp.media = build.json_model
            resp.status = falcon.HTTP_200

class Create(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super(Create, self).on_get(req, resp, *args, **kwargs)



        resp.media = None
        resp.status = falcon.HTTP_200