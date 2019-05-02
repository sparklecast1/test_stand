#!/usr/bin/python3
from collections import defaultdict
import uuid
import pymysql

# Open database connection
db = pymysql.connect("localhost","root","123456Aa","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS search")

# Create table as per requirement
sql_create = """CREATE TABLE search (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data varchar(100),
    last_update date
    );"""

sql_insert = """
    DELIMITER $$
    CREATE PROCEDURE InsertRand(IN NumRows INT, IN MinVal INT, IN MaxVal INT)
        BEGIN
            DECLARE i INT;
            SET i = 1;
            START TRANSACTION;
            WHILE i <= NumRows DO
                INSERT INTO search VALUES (i, MinVal + CEIL(RAND() * (MaxVal - MinVal)), null);
                SET i = i + 1;
            END WHILE;
            COMMIT;
        END$$
    DELIMITER ;

    CALL InsertRand(1111, 2222, 5555);
    """

try:
    cursor.execute(sql_create)
    db.commit()
except:
    db.rollback();
    print("error to connect to database")

cursor.execute(sql_insert)

# Insert data to the table
'''
for i in range(1,500):
    uuid1 = uuid.uuid4().hex
    #print(i, uuid1)
    try:
        #result = cursor.execute("INSERT INTO search (id, data, last_update) VALUES (%s, %s, %s)",  (i, uuid1, None))
        a = a + 1
        #db.commit()
    except db.DatabaseError as err:
        print("Error: ", err)

'''
# disconnect from server
db.close()
