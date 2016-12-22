USE music_db;

DROP TABLE IF EXISTS `artist`;

CREATE TABLE `artist` (
  `id`   INT(11)     NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idartist_UNIQUE` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `album`;

CREATE TABLE `album` (
  `id`           INT(11) NOT NULL AUTO_INCREMENT,
  `artist_id`    INT(11)          DEFAULT NULL,
  `name`         VARCHAR(45)      DEFAULT NULL,
  `release_date` YEAR(4)          DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `artist_album`;

CREATE TABLE `artist_album` (
  `id`        INT(11) NOT NULL AUTO_INCREMENT,
  `artist_id` INT(11)          DEFAULT NULL,
  `album_id`  INT(11)          DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


DROP TABLE IF EXISTS `instrument_album`;

CREATE TABLE `instrument_album` (
  `id`       INT(11) NOT NULL AUTO_INCREMENT,
  `album_id` INT(11)          DEFAULT NULL,
  `piano`    CHAR(1)          DEFAULT 'f',
  `guitar`   CHAR(1)          DEFAULT 'f',
  `bass`     CHAR(1)          DEFAULT 'f',
  `drums`    CHAR(1)          DEFAULT 'f',
  `horns`    CHAR(1)          DEFAULT 'f',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--DROP TABLE IF EXISTS `song`;
--
--CREATE TABLE `song` (
--  `id`       INT(11) NOT NULL AUTO_INCREMENT,
--  `name`     VARCHAR(45)      DEFAULT NULL,
--  `duration` TIME             DEFAULT NULL,
--  PRIMARY KEY (`id`)
--)
--  ENGINE = InnoDB
--  DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `track`;

CREATE TABLE `track` (
  `id`       INT(11) NOT NULL AUTO_INCREMENT,
  `name`     VARCHAR(45)      DEFAULT NULL,
  `album_id` INT(11)          DEFAULT NULL,
  `duration` TIME             DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
