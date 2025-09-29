-- Insert testing user
WITH user_id AS (
	INSERT INTO hot_takes.users (user_id)
	VALUES ('00000000-0000-0000-0000-000000000000')
	RETURNING user_id
)
INSERT INTO hot_takes.user_accounts (user_id, username)
VALUES ((SELECT * FROM user_id), 'testuser');
