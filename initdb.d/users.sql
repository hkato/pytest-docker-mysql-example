CREATE TABLE IF NOT EXISTS users
(
  id INTEGER NOT NULL,
  name VARCHAR(50),
  fullname VARCHAR(50),
  nickname VARCHAR(50),
  PRIMARY KEY (id)
);

-- 
-- テストデータ
-- 実際はシェルスクリプトでCSVをLOAD DATA INFILEすると吉
--
INSERT INTO users (id, name, fullname, nickname) VALUES (1, 'ed', 'Ed Jones', 'edsnickname');
INSERT INTO users (id, name, fullname, nickname) VALUES (2, 'wendy', 'Wendy Williams', 'windy');
INSERT INTO users (id, name, fullname, nickname) VALUES (3, 'mary', 'Mary Contrary', 'mary');
INSERT INTO users (id, name, fullname, nickname) VALUES (4, 'fred', 'Fred Flintstone', 'freddy');
