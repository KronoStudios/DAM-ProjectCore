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

# @falcon.before(requires_auth)
class Get(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Get, self).on_get(req, resp, *args, **kwargs)

        cards = { "cards": [] }
        for c in self.db_session.query(Card).all():
            cards["cards"].append(c.json_model) 

        resp.media = cards
        resp.status = falcon.HTTP_200

# @falcon.before(requires_auth)
class Find(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Find, self).on_get(req, resp, *args, **kwargs)

        card = self.db_session.query(Card).filter(Card.id == kwargs["card"]).one_or_none()

        if card is None:
            resp.status = falcon.HTTP_404
        else:
            resp.media = card.json_model
            resp.status = falcon.HTTP_200
            
            
# @falcon.before(requires_auth)
class Create(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Get, self).on_get(req, resp, *args, **kwargs)
        game = Game(user1_id = req.user1_id, user2_id = req.user2_id, user_winner_id = req.user_winner_id)
        
        self.db_session.add(game)
        self.db_session.commit()
        self.db_session.close()
        
        resp.media = "success"
        resp.status = falcon.HTTP_200
        
        
# @falcon.before(requires_auth)
class FindGameListByUser(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(Find, self).on_get(req, resp, *args, **kwargs)

        games = { "games": [] }
        for c in self.db_session.query(Game).filter(Game.user1_id == kwargs["user"] or Game.user2_id == kwargs["user"]):
            games["games"].append(c.json_model) 

        resp.media = games
        resp.status = falcon.HTTP_200