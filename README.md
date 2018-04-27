数据库采用的是tornadb,

CREATE TABLE IF NOT EXISTS `user`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `name` VARCHAR(100) NOT NULL,
   `password` VARCHAR(40) NOT NULL,
   `email` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


Create table user_authcode(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `verification_status` boolean not null default '0’,
   `authcode` VARCHAR(100) NOT NULL,
   `token` VARCHAR(40) NOT NULL,
)