SELECT * FROM vk_bot_ticket_creator.messages 
	WHERE LOCATE(TRIM(LOWER("mode")), mode) > 0 or LOCATE(TRIM(LOWER("mode")), message) > 0;