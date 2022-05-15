#!/usr/bin/python
# -*- coding: utf-8 -*-

SchemaUserToken = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
    },
    "required": ["token"]
}

SchemaRegisterUser = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
        "name": {"type": "string"}
    },
    "required": ["username", "password", "email", "name"]
}

SchemaRegisterGame = {
    "type": "object",
    "properties": {
        "user1_id": {"type": "string"},
        "user2_id": {"type": "string"},
        "user_winner_id": {"type": "string"},
    },
    "required": ["user1_id", "user2_id", "user_winner_id"]
}