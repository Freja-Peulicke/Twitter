DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id                  TEXT,
    username            TEXT,
    name                TEXT,
    last_name           TEXT,
    total_followers     TEXT,
    total_following     TEXT,
    total_tweets        TEXT,
    avatar              TEXT,

    PRIMARY KEY(id)
    ) WITHOUT ROWID;


INSERT INTO users VALUES("ccec0766e15a476f939058b13563b8b2", "elonmusk", "Elon", "Musk", "1298900000", "177", "22700","ccec0766e15a476f939058b13563b8b2.jpg");
INSERT INTO users VALUES("bd17f1a11c2d462c8bd73ad28ed5b680", "shakira", "Shakira", "", "53700000", "235", "7999","bd17f1a11c2d462c8bd73ad28ed5b680.jpg");
INSERT INTO users VALUES("a1e871848d5b41c59ae4cafa7b907503", "michelleobama", "michelle", "obama", "222000000", "17", "2182","a1e871848d5b41c59ae4cafa7b907503.jpg");
