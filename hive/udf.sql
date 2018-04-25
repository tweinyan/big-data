
CREATE table u(
    fname STRING,
    lname STRING
);

insert into table u values('asdf', 'asdf');
insert into table u values('asdf2', 'asdf');
insert into table u values('asdf3', 'asdf');
insert into table u values('asdf4', 'asdf');

hadoop fs -put udf.py /user/hive/lib/
ADD FILE hdfs:///user/hive/lib/udf.py;

SELECT TRANSFORM(fname, lname) USING 'udf.py' AS (fname, l_name) FROM u;
SELECT TRANSFORM(fname, lname) USING 'python2.6 udf.py' AS (fname, l_name) FROM u;


USE twein_test;
CREATE TABLE foo (id INT, vtype STRING, price FLOAT);
INSERT INTO TABLE foo VALUES (1, "car", 1000.);
INSERT INTO TABLE foo VALUES (2, "car", 42.);
INSERT INTO TABLE foo VALUES (3, "car", 10000.);
INSERT INTO TABLE foo VALUES (4, "car", 69.);
INSERT INTO TABLE foo VALUES (5, "bike", 1426.);
INSERT INTO TABLE foo VALUES (6, "bike", 32.);
INSERT INTO TABLE foo VALUES (7, "bike", 1234.);
INSERT INTO TABLE foo VALUES (8, "bike", null);

--------------------udaf--------------------
pip install virtualenv
virtualenv --on-site-packages -p /usr/bin/python2.6 venv

-p: 指定使用的python版本号
source venv/bin/activate
pip install pandas

cd venv
tar zcvfh ../penv27.tar ./
"-h"的参数:它会把符号链接文件视作普通文件或目录，从而打包的是源文件

hadoop fs -put penv27.tar /user/hive/lib/
hadoop fs -ls /user/hive/lib
hadoop fs -put udaf.py /user/hive/lib/
hadoop fs -put udaf.sh /user/hive/lib

DELETE ARCHIVE hdfs:///user/hive/lib/penv27.tar;
ADD ARCHIVE hdfs:///user/hive/lib/penv27.tar;
DELETE FILE hdfs:///user/hive/lib/udaf.py;
ADD FILE hdfs:///user/hive/lib/udaf.py;
DELETE FILE hdfs:///user/hive/lib/udaf.sh;
ADD FILE hdfs:///user/hive/lib/udaf.sh;

USE test;
SELECT TRANSFORM(id, vtype, price) USING 'udaf.sh' AS (vtype STRING, mean FLOAT, var FLOAT) FROM (SELECT * FROM foo CLUSTER BY vtype) AS TEMP_TABLE;
