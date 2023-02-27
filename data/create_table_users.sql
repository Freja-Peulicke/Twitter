DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id                  TEXT,
    username            TEXT,
    first_name          TEXT,
    last_name           TEXT,
    total_followers     TEXT,
    total_following     TEXT,
    total_tweets        INT,
    avatar              TEXT,
    created_at          TEXT,
    total_retweets      TEXT,
    total_comments      TEXT,
    total_likes         TEXT,
    total_dislikes      TEXT,

    PRIMARY KEY(id)
    ) WITHOUT ROWID;


INSERT INTO users VALUES("ccec0766e15a476f939058b13563b8b2", "elonmusk", "Elon", "Musk", "1298900000", "177", "22700","ccec0766e15a476f939058b13563b8b2", "0", "0", "0","0", "0");
INSERT INTO users VALUES("bd17f1a11c2d462c8bd73ad28ed5b680", "shakira", "Shakira", "", "53700000", "235", "7999","bd17f1a11c2d462c8bd73ad28ed5b680", "0", "0", "0","0", "0");
INSERT INTO users VALUES("a1e871848d5b41c59ae4cafa7b907503", "michelleobama", "Michelle", "Obama", "222000000", "17", "2182","a1e871848d5b41c59ae4cafa7b907503", "0", "0", "0","0","0");



--##### Tweets 

DROP TABLE IF EXISTS tweets;

CREATE TABLE tweets(
    id          TEXT,
    message     TEXT,
    image       TEXT,
    created_at  TEXT,
    user_fk     TEXT,
    replies     TEXT DEFAULT 0,
    retweets    TEXT DEFAULT 0,
    likes       TEXT DEFAULT 0,
    views       TEXT DEFAULT 0,

    PRIMARY KEY(id)
    )WITHOUT ROWID;

INSERT INTO tweets VALUES ("fdf9bd43492641d7a0df94c543379a2e","","ec07a720fa2441b6a9e69b1636183a31","1677099006","ccec0766e15a476f939058b13563b8b2","27200", "493000", "5659000","857000000");
INSERT INTO tweets VALUES ("5160b233a2e3478d9abfe6a977a79fb7","High time I confessed I let the Doge out","99b43aa0abe04561a90debed1c436a94","1677081006","ccec0766e15a476f939058b13563b8b2","14700","20400","235000","474000000");
INSERT INTO tweets VALUES ("bf2dc070e60341f59b03ffdb41611f51","Fact check me @CommunityNotes","","1677042856","ccec0766e15a476f939058b13563b8b2","1652","1370","17300","5200000");
INSERT INTO tweets VALUES ("d590dd6c61964a5aa1eaa7bce00be7c8","Many go woke for the moral cloak","","1677039263","ccec0766e15a476f939058b13563b8b2", "8714","16200", "1636000", "399000000");
INSERT INTO tweets VALUES ("f6659fcfe3284275aa29ca9cfa6de47f","Turning judgment from metoo you","","1677035663","ccec0766e15a476f939058b13563b8b2", "1492","1857","26100","41000000");
INSERT INTO tweets VALUES ("a98523bbed714d4ea7444347340c1c8a","Nice work by Community Notes team! In general Community Notes is a game changer for combating wrong information.","","1677028463","ccec0766e15a476f939058b13563b8b2","2792", "4546", "49700", "586000000");

INSERT INTO tweets VALUES (
"99b43aa0abe04561a90debed1c436a94",
"Limmie – I’m so glad you're performing again at the Opera. Your story and your incredible voice will inspire so many people around the world. #BlackHistoryMonth",
"a15e880f0e544a569eb0e154bdcb2a2e",
"1676667006",
"a1e871848d5b41c59ae4cafa7b907503",
"182",
"646",
"6317",
"613800"
);

INSERT INTO tweets VALUES (
"7686c830f91949e3bc3fdcbcd19f610e",
"I couldn’t be more grateful for the work that our nation’s school counselors do every day for our students. Congratulations to Meredith Draughn, an elementary school counselor in North Carolina, who is the 2023 @ASCAtweets School Counselor of the Year! #ReachHigher",
"e5f7d10d49b6420689fc4e73717581eb",
"1676580606",
"a1e871848d5b41c59ae4cafa7b907503",
"206",
"590",
"7056",
"7826000"
);
INSERT INTO tweets VALUES (
"bfe8ebfb38744331a89836dad256e182",
"Happy Valentine’s Day, @BarackObama! I couldn’t have asked for a better partner to navigate life with. Love you! 💘 Photo credit: Amos Jackson III",
"060c3687f88c4a8ea5e855b4a0e210a3",
"1676407806",
"a1e871848d5b41c59ae4cafa7b907503",
"5256",
"10100",
"237200",
"7000000"
);
INSERT INTO tweets VALUES (
"7de1ce17bdf74a3e9c122e30088b3c28",
"For me, the practice I’ve had—and the effort I make—in finding and appreciating the light inside of other people has become one of my most valuable tools for overcoming uncertainty and keeping my hopefulness intact. #TheLightWeCarry",
"",
"1675111806",
"a1e871848d5b41c59ae4cafa7b907503",
"75",
"243",
"2280",
"460300"
);
INSERT INTO tweets VALUES (
"102e2d74aea54686ac837dafebeb6bd7",
"I'd love to hear from you. What's a practice or purpose that lifts you up? #TheLightWeCarry",
"",
"1675074606",
"a1e871848d5b41c59ae4cafa7b907503",
"347",
"211",
"1460",
"462000"
);

INSERT INTO tweets VALUES (
"6d044afa28844f198a86b782a0bd59fc",
"Gracias a todos por la increíble recepción a tqg  💛💙❤️",
"e27185460ff14db493a28540d1590d69",
"1677266227",
"bd17f1a11c2d462c8bd73ad28ed5b680",
"1433",
"4066",
"61100",
"897300"
);
INSERT INTO tweets VALUES (
"74d1ebba9fec41019663e27a2ef8242a",
"Muchísimas gracias a mi gente, a @premiolonuestro y a @Univision por estos tres reconocimientos y por el apoyo de siempre, gracias de corazón! #PremioLoNuestro",
"6bce0880415241b9a226caaf9f8a63fe",
"1677248427",
"bd17f1a11c2d462c8bd73ad28ed5b680",
"348",
"1178",
"15000",
"3723000"
);
INSERT INTO tweets VALUES (
"884859958ebb4fb49c924b3c7ad0bca8",
"Feliz cumple @karolg! 🥰🥳😘",
"",
"1676384427",
"bd17f1a11c2d462c8bd73ad28ed5b680",
"1920",
"6248",
"165900",
"71000000"
);
INSERT INTO tweets VALUES (
"4cc4c59fa56e4f409b4d29304a3facce",
"Remembering good times and wishing you the best vibes for tonight’s show, Rih! 🥰 @rihanna #SBLVII #AppleMusicHalftime",
"62a85b67216442bab4ba19b59f56af38",
"1676384427",
"bd17f1a11c2d462c8bd73ad28ed5b680",
"1509",
"24300",
"3469000",
"11100000"
);