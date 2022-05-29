#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from db.models import Game, User, Token

import falcon
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from hooks import requires_auth
import messages
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaRegisterGame

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
        #game = Game(user1_id = req.user1_id, user2_id = req.user2_id, user_winner_id = req.user_winner_id)
        game = Game()
        
        #user1_id is now a token
        token = req.user1_id
        print("token==" + str(token))
        current_user = self.db_session.query(Token).filter(Token.token == token).one_or_none()
        print("current_user.user_id==" + str(current_user.user_id))
        user1id = current_user.user_id

        game.user1_id = user1id
        game.user2_id = req.user2_id
        print("game.user2_id==" + str(game.user2_id))
        
        #calculate user_winner_id
        if req.user_winner_id == 1:
            game.user_winner_id = game.user1_id
        else:
            game.user_winner_id = game.user2_id

        print("game.user_winner_id==" + str(game.user_winner_id))
        
        self.db_session.add(game)
        self.db_session.commit()
        self.db_session.close()
        
        resp.media = "success"
        resp.status = falcon.HTTP_200
        
        
# @falcon.before(requires_auth)
class FindGameListByUser(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(FindGameListByUser, self).on_get(req, resp, *args, **kwargs)

        token = req.get_header("Authorization")

        print(token)
        current_user = self.db_session.query(Token).filter(Token.token == token).one_or_none()
        userid = current_user.user_id

        arr = []
        for c in self.db_session.query(Game).filter( (Game.user1_id == userid)):
            arr.append(c.json_model) 

        #fem 2 for's, per que per alguna raó no ens deixava posar dues condicions dins el filter()
        for c in self.db_session.query(Game).filter( (Game.user2_id == userid)):
            arr.append(c.json_model) 
 
        arr = sorted(arr, key=lambda x : x['played_at'], reverse=True)
        games = { "games": arr }

        resp.media = games
        resp.status = falcon.HTTP_200
        
# @falcon.before(requires_auth)
class ResourceRegisterGame(DAMCoreResource):
    #@jsonschema.validate(SchemaRegisterGame)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceRegisterGame, self).on_post(req, resp, *args, **kwargs)

        try:
            print(req.media)
            
            #aux_game = Game(user1_id = req.user1_id, user2_id = req.user2_id, user_winner_id = req.user_winner_id)
            
            game = Game()



            #user1_id is now a token
            token = req.media["user1_id"]
            current_user = self.db_session.query(Token).filter(Token.token == token).one_or_none()
            user1id = current_user.user_id

            game.user1_id = user1id
            game.user2_id = req.media["user2_id"]
            
            #calculate user_winner_id
            if req.media["user_winner_id"] == '1':
                game.user_winner_id = game.user1_id
            else:
                game.user_winner_id = game.user2_id

            print("game.user_winner_id==" + str(game.user_winner_id))
            
            self.db_session.add(game)

            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest(description=messages.game_exists)

        except KeyError:
            raise falcon.HTTPBadRequest(description=messages.parameters_invalid)

        resp.status = falcon.HTTP_200
