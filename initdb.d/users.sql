CREATE TABLE IF NOT EXISTS users
(
  id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(128),
  PRIMARY KEY (id)
);

-- 
-- テストデータ
-- 実際はシェルスクリプトでCSVをLOAD DATA INFILEすると吉
--
INSERT INTO users (id, name) VALUES (1, 'Yamada Taro');
INSERT INTO users (id, name) VALUES (2, 'Hanako Sato');
