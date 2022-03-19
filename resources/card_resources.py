#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from db.models import Card

import falcon
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from hooks import requires_auth

import messages
from resources.base_resources import DAMCoreResource

mylogger = logging.getLogger(__name__)

#@falcon.before(requires_auth)
class Get(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Get, self).on_get(req, resp, *args, **kwargs)

        cards = { "cards": [] }
        for c in self.db_session.query(Card).all():
            cards["cards"].append(c.json_model) 

        resp.media = cards
        resp.status = falcon.HTTP_200

class Find(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Find, self).on_get(req, resp, *args, **kwargs)

        card = self.db_session.query(Card).filter(Card.id == kwargs["card"]).one_or_none()

        if card is None:
            resp.status = falcon.HTTP_404
        else:
            resp.media = card.json_model
            resp.status = falcon.HTTP_200