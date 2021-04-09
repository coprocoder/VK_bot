#create database VK_bot_ticket_creator;
USE VK_bot_ticket_creator;
#DROP TABLE VK_bot_ticket_creator.messages;
CREATE TABLE VK_bot_ticket_creator.messages (
		`mes_id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
		`mode` VARCHAR(100)  NOT NULL,
        `user_id` MEDIUMINT UNSIGNED NOT NULL,
        `group_id` MEDIUMINT UNSIGNED NOT NULL,
        `message` LONGTEXT  NOT NULL,
        PRIMARY KEY(`mes_id`)
        );