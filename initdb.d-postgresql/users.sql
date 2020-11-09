CREATE TABLE IF NOT EXISTS users
(
  id SERIAL NOT NULL,
  name VARCHAR(128),
  PRIMARY KEY (id)
);

--
-- テストデータ
-- 実際はシェルスクリプトでCSVをCOPY FROMすると吉
--
INSERT INTO users (id, name) VALUES (1, 'Yamada Taro');
INSERT INTO users (id, name) VALUES (2, 'Hanako Sato');
