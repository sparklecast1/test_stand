#!/bin/bash
docker exec -i mysql mysql -p123456Aa -e "
DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
USE test;
CREATE TABLE search (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  data VARCHAR(100),
  last_update date
);
"

echo "test"
for ((i=1; i < 500; i++))
#for i in 1 2 3...500
do
    UUID=$(cat /proc/sys/kernel/random/uuid)
    docker exec -i mysql mysql -p123456Aa --database=test -e "
    INSERT INTO search (id, data, last_update) VALUES ('$i','$UUID', null);
    ";
    echo $i + $UUID;
done
