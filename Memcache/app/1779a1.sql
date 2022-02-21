CREATE DATABASE `estore`;

USE `estore`;

Drop TABLE if exists image;
Drop TABLE if exists statistics;
Drop TABLE if exists config;

CREATE TABLE `image`(
	`image_id` INT AUTO_INCREMENT,
    `image_name` VARCHAR(45) NOT NULL,
    `image_location` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`image_id`)
);

CREATE TABLE `statistics`(
	`timestamp` DATETIME(6),
    `num_item` SMALLINT,
    `size` INT,
    `num_request` INT,
    `num_miss` INT,
    PRIMARY KEY (`timestamp`)
);

CREATE TABLE `config`(
	`id` TINYINT AUTO_INCREMENT,
    `capacity` INT,
    `replace_policy` VARCHAR(10),
    PRIMARY KEY (`id`)
);

INSERT INTO `statistics` (`timestamp`, `num_item`, `size`, `num_request`, `num_miss`) VALUES (NOW(), 0, 0, 0, 0);

# get utilization statistics
SELECT `timestamp`, `num_item`, `size`, `num_request`, `num_miss` FROM statistics;
# update configure
UPDATE `config` SET `capacity` = 1, `replace_policy` = 'Random';
# get configure
SELECT `capacity`, `replace_policy` FROM `config`;
# write utilization statistics
INSERT INTO `statistics` (`timestamp`, `num_item`, `size`, `num_request`, `num_miss`) VALUES (NOW(), %s, %s, %s, %s);




