#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import os

from sqlalchemy.sql import text

import db
import settings
from db.models import SQLAlchemyBase, User, Card, Character, Build, BuildCardAssociation
from settings import DEFAULT_LANGUAGE

from faker import Faker

# LOGGING
mylogger = logging.getLogger(__name__)
settings.configure_logging()

fake = Faker()


def execute_sql_file(sql_file):
    sql_folder_path = os.path.join(os.path.dirname(__file__), "sql")
    sql_file_path = open(os.path.join(sql_folder_path, sql_file), encoding="utf-8")
    sql_command = text(sql_file_path.read())
    db_session.execute(sql_command)
    db_session.commit()
    sql_file_path.close()


if __name__ == "__main__":
    settings.configure_logging()

    db_session = db.create_db_session()

    # -------------------- REMOVE AND CREATE TABLES --------------------
    mylogger.info("Removing database...")
    SQLAlchemyBase.metadata.drop_all(db.DB_ENGINE)
    mylogger.info("Creating database...")
    SQLAlchemyBase.metadata.create_all(db.DB_ENGINE)

    if db_session.query(Card).count() == 0:
        for i in range(100):
            c = Card(name = fake.word(), description = fake.sentence(), java_class = "com.kronostudios.the_game.cards.Fireball", image = "")
            db_session.add(c)

    if db_session.query(User).count() == 0:
        for i in range(10):
            u = User(username = fake.user_name(), email = fake.email())
            u.set_password("1234")
            db_session.add(u)

            b = Build(name = fake.sentence(2), user = u)
            a = BuildCardAssociation(card = c, amount = 9)
            b.cards.append(a)
            db_session.add(b)
            
            for j in range(3):
                char = Character(build = b, name = fake.name())
                db_session.add(char)

    db_session.commit()
    db_session.close()