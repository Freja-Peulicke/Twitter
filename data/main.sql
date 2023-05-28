-- PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
  user_id                     TEXT NOT NULL UNIQUE,
  user_email                  TEXT NOT NULL UNIQUE,
  user_phone                  TEXT NOT NULL UNIQUE,
  user_name                   TEXT NOT NULL UNIQUE,
  user_gold_key               TEXT NOT NULL,
  user_password               TEXT NOT NULL,
  user_first_name             TEXT NOT NULL,
  user_last_name              TEXT DEFAULT "",
  user_verified_at            INT  DEFAULT 0,
  user_created_at             INT  NOT NULL, 
  user_gold_at                INT  DEFAULT 0,
  user_activated_at           INT  DEFAULT 0,
  user_banner                 TEXT DEFAULT "",
  user_avatar                 TEXT DEFAULT "", 
  user_total_tweets           INT  DEFAULT 0,
  user_total_followers        INT  DEFAULT 0,
  user_total_following        INT  DEFAULT 0,
  user_blocked_until          INT  DEFAULT 0,
  user_archived_at            INT  DEFAULT 0,
  PRIMARY KEY(user_id)
) WITHOUT rowid;

INSERT INTO users VALUES("ccec0766e15a476f939058b13563b8b2","elonmusk@gmail.com","11111111", "elonmusk","1234","$2b$12$WQ9GwPD2lmP3ZbUNWM7gMOaoX26xkyj4vYlZPBypOwwpJpNOl9HhS", "Elon", "Musk",0, 1298900000,0,0, "ccec0766e15a476f939058b13563b8b2.jpg", "ccec0766e15a476f939058b13563b8b2.jpg",177, 0, 0, 0,0);
INSERT INTO users VALUES("bd17f1a11c2d462c8bd73ad28ed5b680","shakira@gmail.com","22222222", "shakira","1234","$2b$12$WQ9GwPD2lmP3ZbUNWM7gMOaoX26xkyj4vYlZPBypOwwpJpNOl9HhS", "Shakira", "",0, 1298900340,0,0, "bd17f1a11c2d462c8bd73ad28ed5b680.jpg", "bd17f1a11c2d462c8bd73ad28ed5b680.jpg",200, 0, 0, 0,0);
INSERT INTO users VALUES("a1e871848d5b41c59ae4cafa7b907503","michelleobama@gmail.com","33333333", "michelleobama","1234","$2b$12$WQ9GwPD2lmP3ZbUNWM7gMOaoX26xkyj4vYlZPBypOwwpJpNOl9HhS", "Michelle", "Obama",0, 1298900340,0,0, "a1e871848d5b41c59ae4cafa7b907503.jpg", "a1e871848d5b41c59ae4cafa7b907503.jpg",2050, 0, 0, 0,0);

CREATE UNIQUE INDEX idx_users_username ON users(user_name);

CREATE INDEX idx_users_user_first_name ON users(user_first_name);
CREATE INDEX idx_users_user_last_name ON users(user_last_name);
CREATE INDEX idx_users_user_avatar ON users(user_avatar);

DROP TABLE IF EXISTS followers;
CREATE TABLE followers (
follower_fk         TEXT,
followee_fk         TEXT,
followed_at         INT NOT NULL 
);

-- Tweets 
DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets(
  tweet_id          TEXT NOT NULL UNIQUE,
  tweet_message     TEXT DEFAULT "",
  tweet_image       TEXT DEFAULT "",
  tweet_retweet_fk  TEXT DEFAULT "",
  tweet_created_at  INT  NOT NULL,
  tweet_user_fk     TEXT NOT NULL,
  tweet_replies     INT  DEFAULT 0,
  tweet_retweets    INT  DEFAULT 0,
  tweet_likes       INT  DEFAULT 0,
  tweet_views       INT  DEFAULT 0,
  PRIMARY KEY(tweet_id),
  FOREIGN KEY(tweet_user_fk) REFERENCES users(user_id)
) WITHOUT ROWID;

-- Full Text Search - Virtual Table
DROP TABLE IF EXISTS tweets_fts;
CREATE VIRTUAL TABLE tweets_fts USING fts5 
(
  tweet_message,
  tweet_id UNINDEXED
);

CREATE TRIGGER tweets_fts_insert AFTER INSERT ON tweets
BEGIN
    INSERT INTO tweets_fts (tweet_message, tweet_id) VALUES (new.tweet_message, new.tweet_id);
END;

CREATE TRIGGER tweets_fts_delete AFTER DELETE ON tweets
BEGIN
    INSERT INTO tweets_fts (tweets_fts, tweet_message, tweet_id) VALUES ('delete', old.tweet_message, old.tweet_id);
END;

DROP TRIGGER IF EXISTS tweets_fts_update;

CREATE TRIGGER tweets_fts_update AFTER UPDATE ON tweets
BEGIN
  DELETE FROM tweets_fts WHERE tweet_id = old.tweet_id;

  INSERT INTO tweets_fts (tweet_message, tweet_id) VALUES (new.tweet_message, new.tweet_id);
END;


INSERT INTO tweets VALUES ("fdf9bd43492641d7a0df94c543379a2e","","ec07a720fa2441b6a9e69b1636183a31.jpg","",1677099006,"ccec0766e15a476f939058b13563b8b2", 27200, 493000, 5659000, 857000000);
INSERT INTO tweets VALUES ("5160b233a2e3478d9abfe6a977a79fb7","High time I confessed I let the Doge out","99b43aa0abe04561a90debed1c436a94.jpg","",1677081006,"ccec0766e15a476f939058b13563b8b2",14700, 20400, 235000, 474000000);
INSERT INTO tweets VALUES ("bf2dc070e60341f59b03ffdb41611f51","Fact check me @CommunityNotes","","",1677042856,"ccec0766e15a476f939058b13563b8b2", 1652, 1370, 17300, 5200000);
INSERT INTO tweets VALUES ("d590dd6c61964a5aa1eaa7bce00be7c8","Many go woke for the moral cloak","","",1677039263,"ccec0766e15a476f939058b13563b8b2", 8714,16200, 1636000, 399000000);
INSERT INTO tweets VALUES ("f6659fcfe3284275aa29ca9cfa6de47f","Turning judgment from metoo you","","",1677035663,"ccec0766e15a476f939058b13563b8b2",  1492 , 1857 , 26100 , 41000000 );
INSERT INTO tweets VALUES ("a98523bbed714d4ea7444347340c1c8a","Nice work by Community Notes team! In general Community Notes is a game changer for combating wrong information.","","",1677028463,"ccec0766e15a476f939058b13563b8b2", 2792 ,  4546 ,  49700 ,  586000000 );

INSERT INTO tweets VALUES (
"99b43aa0abe04561a90debed1c436a94",
"Limmie – I’m so glad you're performing again at the Opera. Your story and your incredible voice will inspire so many people around the world. #BlackHistoryMonth",
"a15e880f0e544a569eb0e154bdcb2a2e.jpg",
"",
1676667006,
"a1e871848d5b41c59ae4cafa7b907503",
182,
646,
6317,
613800
);

INSERT INTO tweets VALUES (
"7686c830f91949e3bc3fdcbcd19f610e",
"I couldn’t be more grateful for the work that our nation’s school counselors do every day for our students. Congratulations to Meredith Draughn, an elementary school counselor in North Carolina, who is the 2023 @ASCAtweets School Counselor of the Year! #ReachHigher",
"e5f7d10d49b6420689fc4e73717581eb.jpg",
"",
1676580606,
"a1e871848d5b41c59ae4cafa7b907503",
206,
590,
7056,
7826000
);
INSERT INTO tweets VALUES (
"bfe8ebfb38744331a89836dad256e182",
"Happy Valentine’s Day, @BarackObama! I couldn’t have asked for a better partner to navigate life with. Love you! 💘 Photo credit: Amos Jackson III",
"060c3687f88c4a8ea5e855b4a0e210a3.jpg",
"",
1676407806,
"a1e871848d5b41c59ae4cafa7b907503",
5256,
10100,
237200,
7000000
);
INSERT INTO tweets VALUES (
"7de1ce17bdf74a3e9c122e30088b3c28",
"For me, the practice I’ve had—and the effort I make—in finding and appreciating the light inside of other people has become one of my most valuable tools for overcoming uncertainty and keeping my hopefulness intact. #TheLightWeCarry",
"",
"",
1675111806,
"a1e871848d5b41c59ae4cafa7b907503",
75,
243,
2280,
460300
);
INSERT INTO tweets VALUES (
"102e2d74aea54686ac837dafebeb6bd7",
"I'd love to hear from you. What's a practice or purpose that lifts you up? #TheLightWeCarry",
"",
"",
1675074606,
"a1e871848d5b41c59ae4cafa7b907503",
347,
211,
1460,
462000
);

INSERT INTO tweets VALUES (
"6d044afa28844f198a86b782a0bd59fc",
"Gracias a todos por la increíble recepción a tqg  💛💙❤️",
"e27185460ff14db493a28540d1590d69.jpg",
"",
1677266227,
"bd17f1a11c2d462c8bd73ad28ed5b680",
1433,
4066,
61100,
897300
);
INSERT INTO tweets VALUES (
"74d1ebba9fec41019663e27a2ef8242a",
"Muchísimas gracias a mi gente, a @premiolonuestro y a @Univision por estos tres reconocimientos y por el apoyo de siempre, gracias de corazón! #PremioLoNuestro",
"6bce0880415241b9a226caaf9f8a63fe.jpg",
"",
1677248427,
"bd17f1a11c2d462c8bd73ad28ed5b680",
348,
1178,
15000,
3723000
);
INSERT INTO tweets VALUES (
"884859958ebb4fb49c924b3c7ad0bca8",
"Feliz cumple @karolg! 🥰🥳😘",
"",
"",
1676384427,
"bd17f1a11c2d462c8bd73ad28ed5b680",
1920,
6248,
165900,
71000000
);
INSERT INTO tweets VALUES (
"4cc4c59fa56e4f409b4d29304a3facce",
"Remembering good times and wishing you the best vibes for tonight’s show, Rih! 🥰 @rihanna #SBLVII #AppleMusicHalftime",
"62a85b67216442bab4ba19b59f56af38.jpg",
"",
1676384427,
"bd17f1a11c2d462c8bd73ad28ed5b680",
1509,
24300,
3469000,
11100000
);

INSERT INTO tweets VALUES (
"e27185460ff14db493a28540d1590d69",
"",
"",
"4cc4c59fa56e4f409b4d29304a3facce",
1677266226,
"bd17f1a11c2d462c8bd73ad28ed5b680",
1433,
4066,
61100,
897300
);
-- Comments
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  comment_id              TEXT NOT NULL UNIQUE,
  comment_user_fk         TEXT NOT NULL,
  comment_tweet_fk        TEXT,
  comment_comment_fk      TEXT,
  comment_message         TEXT NOT NULL,
  comment_image           TEXT DEFAULT "",
  comment_created_at      INT NOT NULL,
  comment_replies         INT DEFAULT 0, 
  comment_retweets        INT DEFAULT 0, 
  comment_likes           INT DEFAULT 0, 
  comment_views           INT DEFAULT 0,
  PRIMARY KEY(comment_id)
) WITHOUT ROWID;

-- Likes
DROP TABLE IF EXISTS likes;
CREATE TABLE likes (
  like_id                  TEXT NOT NULL UNIQUE,
  like_user_fk             TEXT NOT NULL,
  like_tweet_fk            TEXT,
  like_comment_fk          TEXT,
  like_created_at          INT NOT NULL,
  PRIMARY KEY(like_id)
) WITHOUT ROWID;


-- Triggers

-- Increase user_total_tweets when a tweet is inserted/created
DROP TRIGGER IF EXISTS increment_user_total_tweets;
CREATE TRIGGER increment_user_total_tweets AFTER INSERT ON tweets
BEGIN
  UPDATE users 
  SET user_total_tweets =  user_total_tweets + 1 
  WHERE user_id = NEW.tweet_user_fk;
END;

-- Increase user_total_followers when a follow is inserted/created
DROP TRIGGER IF EXISTS increment_user_total_followers;
CREATE TRIGGER increment_user_total_followers AFTER INSERT ON followers
BEGIN
  UPDATE users 
  SET user_total_followers =  user_total_followers + 1 
  WHERE user_id = NEW.followee_fk;
END;

-- Decrease user_total_followers when a follow is removed/deleted
DROP TRIGGER IF EXISTS decrement_user_total_followers;
CREATE TRIGGER decrement_user_total_followers AFTER DELETE ON followers
BEGIN
  UPDATE users 
  SET user_total_followers =  user_total_followers - 1 
  WHERE user_id = OLD.followee_fk;
END;

-- Increase tweet_likes when a like is inserted/created
DROP TRIGGER IF EXISTS increment_tweet_likes;
CREATE TRIGGER increment_tweet_likes AFTER INSERT ON likes
BEGIN
  UPDATE tweets 
  SET tweet_likes = tweet_likes + 1 
  WHERE tweet_id = NEW.like_tweet_fk;
END;

-- Decrease tweet_likes when a like is inserted/created
DROP TRIGGER IF EXISTS decrement_tweet_likes;
CREATE TRIGGER decrement_tweet_likes AFTER DELETE ON likes
BEGIN
  UPDATE tweets 
  SET tweet_likes = tweet_likes - 1 
  WHERE tweet_id = OLD.like_tweet_fk;
END;

-- Blue checkmark verification 

DROP TRIGGER IF EXISTS blue_checkmark;
CREATE TRIGGER blue_checkmark AFTER INSERT ON followers
BEGIN
  UPDATE users 
  SET user_verified_at = strftime('%s','now')
  WHERE user_id = NEW.followee_fk
  AND (
    SELECT COUNT(*) 
    FROM followers 
    WHERE followee_fk = NEW.followee_fk
  ) >= 10;
END;