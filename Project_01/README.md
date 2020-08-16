* $ FLASK_APP=app.py FLASK_DEBUG=true flask run
* $ python -m pip install psycopg2-binary
* $ python -m pip install Flask-Migrate
* $ flask db init
* $ dropdb postgres >>> DROP DATABASE postgres
* $ createdb postgres
* $ flask db migrate
* $ flask db upgrade
* $ flask db downgrade
* $ flask db upgrade

## 

* $ which postgres
* $ psql -U postgres postgres
* $ createdb mydb
* $ dropdb mydb
* $ dropdb <database_name> && createdb <database_name>
* $ psql <dbname>
* $ create table <tableName> ( id , name)
* $ \dt
* $ \d <tableName>
* $ \c <anotherDbName>
* $ \l
* $ \?
* $ psql <dbname> [<username>]
* INSERT INTO <tabelName> (id, name) VALUES (1, "ward");
* SELECT * from <tablename>
* $ db.session.commit()

## 

* CREATE DATABASE `databaseName`
* USE ` `
* CREATE TABLE ` ` (`id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT, `emil`  * VARCHAR(50) NUT NULL)
* DROP TABLE ` `
* RENAME TABLE `old` To `new`
* ALTER TABLE `tableName` ADD COLUMN `emile` VARCHAR(40) NOT NULL
* ---ADD COLUMN FIRST and AFTER---
* ALTER TABLE `tableName` DROP COLUMN `columnName`
* INSERT INTO `tabelName` VALUES (1,""),(2,"")
* DELETE FROM `tablName`
* DELETE FROM `tablName` WHERE id = 2
* UPDATE `tabelName` SET cname = 'go' WHERE id = 1
* SELECT `column`,`column1` FROM `tabelName`
* SELECT * FROM `tabelName`
* SELECT `column`,`column1` FROM `tabelName` WHERE `cid` = 6
* SELECT * FROM `tabelName` WHERE `id` IN (6,1)
* SELECT * FROM `tabelName` WHERE `id` BETWEEN 1 AND 5
* REPLACE INTO `tabelName` VALUES (1,"","") 