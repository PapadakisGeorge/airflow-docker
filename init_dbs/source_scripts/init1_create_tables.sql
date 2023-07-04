CREATE DATABASE IF NOT EXISTS `source_db` CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT ALL ON source_db.* TO 'user'@'%' IDENTIFIED BY 'password';

USE `source_db`;

CREATE TABLE IF NOT EXISTS `source_table` (
    `id`                  int(10) unsigned           NOT NULL AUTO_INCREMENT,
    `source_data`         varchar(250)               NOT NULL,
    PRIMARY KEY (`id`)
);