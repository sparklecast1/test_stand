DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
USE test;
CREATE TABLE search (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data varchar(100),
    last_update date);



DECLARE @i INT;
SET i = 1;
WHILE i <= 500 DO
    INSERT INTO `search` (`id`, `data`, `last_update`) VALUES (i, `test123`, NULL);
    SET i = i + 1;
END WHILE;



