
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
