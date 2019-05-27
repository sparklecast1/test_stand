#!/bin/bash

docker exec -i mysql mysql -p123456Aa -e "
DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
"""
docker exec -i mysql mysql -p123456Aa --database=test  < countries_persons_tables_2012-11-28.sql

docker exec -i mysql mysql -p123456Aa --database=test -e "

CREATE TABLE search (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  surname VARCHAR(100),
  country VARCHAR(100),
  last_update date,
  data VARCHAR(100)
);



DELIMITER $$
CREATE PROCEDURE InsertRand(IN NumRows INT, IN MinVal INT, IN MaxVal INT)
    BEGIN
        DECLARE i INT;
        SET i = 1;
        START TRANSACTION;
        WHILE i <= NumRows DO
           SELECT firstname INTO @firstname FROM persons WHERE RAND()<(SELECT ((1/COUNT(*))*10) FROM persons) ORDER BY RAND() LIMIT 1;
           SELECT lastname INTO @lastname FROM persons WHERE RAND()<(SELECT ((1/COUNT(*))*10) FROM persons) ORDER BY RAND() LIMIT 1;
           SELECT name INTO @country FROM countries ORDER BY RAND() LIMIT 1;


            INSERT INTO search (name,surname,country,last_update,data) VALUES (
            @firstname,
            @lastname,
            @country,
            FROM_UNIXTIME(UNIX_TIMESTAMP('2010-01-01 01:00:00')+FLOOR(RAND()*315360000)),
            MinVal + CEIL(RAND() * (MaxVal - MinVal)));
            SET i = i + 1;
        END WHILE;
        COMMIT;
    END$$
DELIMITER ;

CALL InsertRand(100000, 12345, 98765);

"

echo "test"
#for ((i=1; i < 500; i++))
#for i in 1 2 3...500
#do
#    UUID=$(cat /proc/sys/kernel/random/uuid)
#    docker exec -i mysql mysql -p123456Aa --database=test -e "
#    INSERT INTO search (id, data, last_update) VALUES ('$i','$UUID', null);
#    ";
#    echo $i + $UUID;
#done
