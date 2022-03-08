#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import datetime
import enum
import logging
import os
from _operator import and_
from builtins import getattr
from urllib.parse import urljoin

import falcon
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Date, DateTime, BigInteger, Enum, ForeignKey, Integer, Unicode, \
    UnicodeText, Table, type_coerce, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_i18n import make_translatable

import messages
from db.json_model import JSONModel
import settings

mylogger = logging.getLogger(__name__)

SQLAlchemyBase = declarative_base()
make_translatable(options={"locales": settings.get_accepted_languages()})


def _generate_media_url(class_instance, class_attibute_name, default_image=False):
    class_base_url = urljoin(urljoin(urljoin("http://{}".format(settings.STATIC_HOSTNAME), settings.STATIC_URL),
                                     settings.MEDIA_PREFIX),
                             class_instance.__tablename__ + "/")
    class_attribute = getattr(class_instance, class_attibute_name)
    if class_attribute is not None:
        return urljoin(urljoin(urljoin(urljoin(class_base_url, class_attribute), str(class_instance.id) + "/"),
                               class_attibute_name + "/"), class_attribute)
    else:
        if default_image:
            return urljoin(urljoin(class_base_url, class_attibute_name + "/"), settings.DEFAULT_IMAGE_NAME)
        else:
            return class_attribute


def _generate_media_path(class_instance, class_attibute_name):
    class_path = "/{0}{1}{2}/{3}/{4}/".format(settings.STATIC_URL, settings.MEDIA_PREFIX, class_instance.__tablename__,
                                              str(class_instance.id), class_attibute_name)
    return class_path



class Token(SQLAlchemyBase):
    __tablename__ = "tokens"

    id = Column(BigInteger, primary_key=True)
    token = Column(Unicode(255), nullable=False, unique=True)
    user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    valid_until = Column(DateTime, default=datetime.datetime.now, nullable=True)

    user = relationship("User", back_populates="tokens")



class User(SQLAlchemyBase, JSONModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    username = Column(Unicode(255), nullable=False, unique=True)
    password = Column(UnicodeText, nullable=False)
    rating = Column(Integer, nullable=False, default=0)
    scrap = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    builds = relationship("Build", back_populates="user", cascade="all, delete-orphan")

    @hybrid_property
    def public_profile(self):
        return {
            "username": self.username,
            "rating": self.rating,
            "builds": self.builds,
            "created_at": self.created_at.strftime(settings.DATETIME_DEFAULT_FORMAT),
        }

    @hybrid_method
    def set_password(self, password_string):
        self.password = pbkdf2_sha256.hash(password_string)

    @hybrid_method
    def check_password(self, password_string):
        return pbkdf2_sha256.verify(password_string, self.password)

    @hybrid_method
    def create_token(self):
        if len(self.tokens) < settings.MAX_USER_TOKENS:
            token_string = binascii.hexlify(os.urandom(25)).decode("utf-8")
            aux_token = Token(token = token_string, user = self, created_at = datetime.datetime.now())
            return aux_token
        else:
            raise falcon.HTTPBadRequest(title=messages.quota_exceded, description=messages.maximum_tokens_exceded)

    @hybrid_property
    def json_model(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "rating": self.rating,
            "scrap": self.scrap,
            "created_at": self.created_at.strftime(settings.DATETIME_DEFAULT_FORMAT),
        }



class Card(SQLAlchemyBase, JSONModel):
    __tablename__ = "cards"

    id = Column(BigInteger, primary_key=True)
    java_class = Column(Unicode(255), nullable=False)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    image = Column(Unicode(255), nullable=False)

    @hybrid_property
    def json_model(self):
        return {
            "id": self.id,
            "java_class": self.java_class,
            "name": self.name,
            "description": self.description,
            "image": self.image,
        }



class Build(SQLAlchemyBase, JSONModel):
    __tablename__ = "builds"

    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="builds")
    cards = relationship("BuildCardAssociation", back_populates="build")
    characters = relationship("Character", back_populates="build")

    @hybrid_property
    def json_model(self):
        characters = []
        cards = []

        for char in self.characters:
            characters.append(char.json_model)

        for card in self.cards:
            cards.append({ "card": card.card.json_model, "amount": card.amount })

        return {
            "id": self.id,
            "name": self.name,
            "user": self.user.json_model,
            "characters": characters,
            "cards": cards,
        }



class BuildCardAssociation(SQLAlchemyBase):
    __tablename__ = 'build_card'
    build_id = Column(BigInteger, ForeignKey("builds.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    card_id = Column(BigInteger, ForeignKey("cards.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    amount = Column(Integer, nullable=False, default=1)

    build = relationship("Build", back_populates="cards")
    card = relationship("Card")



class Character(SQLAlchemyBase, JSONModel):
    __tablename__ = "characters"

    id = Column(BigInteger, primary_key=True)
    build_id = Column(BigInteger, ForeignKey("builds.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    name = Column(Unicode(255), nullable=False)
    stamina = Column(Unicode(255), nullable=False, default=1)
    strength = Column(Unicode(255), nullable=False, default=1)
    dexterity = Column(Unicode(255), nullable=False, default=1)
    intellect = Column(Unicode(255), nullable=False, default=1)
    
    build = relationship("Build", back_populates="characters")

    @hybrid_property
    def json_model(self):
        return {
            "id": self.id,
            "build_id": self.build_id,
            "name": self.name,
            "stamina": self.stamina,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "intellect": self.intellect,
        }