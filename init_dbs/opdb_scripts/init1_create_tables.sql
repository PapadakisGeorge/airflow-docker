CREATE DATABASE IF NOT EXISTS `op_events_db` CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT ALL ON op_events_db.* TO 'user'@'%' IDENTIFIED BY 'password';

USE `op_events_db`;

CREATE TABLE IF NOT EXISTS `op_table` (
    `id`                  int(10) unsigned           NOT NULL AUTO_INCREMENT,
    `source_id`           int(10) unsigned           NOT NULL,
    `op_data`             varchar(250)               NOT NULL,
    PRIMARY KEY (`id`)
);