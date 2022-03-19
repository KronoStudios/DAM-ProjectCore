#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from faker import Faker
from db.models import Build, BuildCardAssociation, Card, Character, User

import falcon
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

import messages
from resources.base_resources import DAMCoreResource

mylogger = logging.getLogger(__name__)
fake = Faker()


class ResourceHome(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceHome, self).on_get(req, resp, *args, **kwargs)

        resp.media = messages.welcome_message
        resp.status = falcon.HTTP_200


class ResourcePopulate(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourcePopulate, self).on_get(req, resp, *args, **kwargs)

        if self.db_session.query(Card).count() == 0:
            for i in range(100):
                c = Card(name = fake.word(), description = fake.sentence(), java_class = "com.kronostudios.the_game.cards.Fireball", image = "")
                self.db_session.add(c)

        if self.db_session.query(User).count() == 0:
            for i in range(10):
                u = User(username = fake.user_name(), email = fake.email())
                u.set_password("1234")
                self.db_session.add(u)

                b = Build(name = fake.sentence(2), user = u)
                a = BuildCardAssociation(card = c, amount = 9)
                b.cards.append(a)
                self.db_session.add(b)
                
                for j in range(3):
                    char = Character(build = b, name = fake.name())
                    self.db_session.add(char)

        self.db_session.commit()
