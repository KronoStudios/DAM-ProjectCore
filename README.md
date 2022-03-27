# DAM-ProjectCore

## About

<img align="left" width="100" height="100" src="https://user-images.githubusercontent.com/61190134/76793662-b6b8bd00-67c5-11ea-83b2-efcc9ed462fc.png">

*Instructor*: [Jordi Mateo Fornés](http:jordimateofornes.com)

*Course*: [Grau en Tècniques d'Interacció Digital i de Computació](http://www.grauinteraccioicomputacio.udl.cat/ca/index.html)

*University*: University of Lleida - Campus Igualada - Escola Politècnica Superior

## Description

This project create 3 services using docker and docker-compose.

- **Container 1**: MySQL Server. 
- **Container 2**: Adminer. Adminer (formerly PHPMyAdmin) is a full-featured database management tool written in PHP. Conversely to phpMyAdmin, it consists of a single file ready to deploy to the target server. Adminer is available for MySQL, MariaDB, PostgreSQL, SQLite, MS SQL, Oracle, Firebird, SimpleDB, Elasticsearch, and MongoDB.
- **Container 3**: Custom dockerfile based on Python3.7, where we create a folder to deploy the app, and every time we launch the container we reset and init the SQL Database and we start using gunicorn the Falcon API.

![DAMCORE](https://user-images.githubusercontent.com/61190134/75614085-4f4c0d80-5b35-11ea-9550-9f1d31de366b.png)

## Requirements

- docker
- docker-compose

## How to


```sh
$ cd docker
$ docker-compose up --build  [optional=(-d)]   #Start
$ docker-compose down                          #Stop
```

## Legend
- [A] Indicates that requires Authorization header (token)

## Resources

### Account Resources
- POST /account/create_token
- [A] POST /account/delete_token
- [A] GET /account/profile

### Users Resources
- POST /users/register
- [A] GET /users/show/{username:str}

###  Data Model	

Nuestro modelo consiste de varias tablas donde almacenamos los datos.
<br>
Primero tenemos la tabla users, con un numero identificador, sus datos de login, fecha de creación y su rating.
<br>
La tabla tokens, ligada a users, almacenará los logins.
<br>
La tabla builds es una relación 1..n de users, que luego se relaciona con build_card y characters.
<br>
Por último, la tabla cards, que representan cada carta en el juego, con su nombre, descripción e imagen, y la clase de java que ejecuta su efecto.
<br>
<br>
![DIAGRAMA](https://i.imgur.com/3z8Le4a.png)
