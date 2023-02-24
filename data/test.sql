SELECT users.id AS user_id, message, image, tweets.created_at AS tweet_created_at, replies, retweets, likes, views, username, first_name, last_name FROM tweets JOIN users ON user_fk = users.id ORDER BY RANDOM() LIMIT 5;

SELECT * FROM tweets JOIN users ON user_fk = users.id ORDER BY RANDOM() LIMIT 5;