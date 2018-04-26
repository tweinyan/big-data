user_id article_id event_time

11,101,2016-05-01 06:01:12
22,102,2016-05-01 07:28:12
33,103,2016-05-01 07:50:12
11,104,2016-05-01 09:27:12
22,103,2016-05-01 09:03:12
33,102,2016-05-02 19:10:12
11,101,2016-05-02 09:07:12
35,105,2016-05-03 11:07:12
22,104,2016-05-03 12:59:12
77,103,2016-05-03 18:04:12
99,102,2016-05-04 00:36:39
33,101,2016-05-04 19:10:12
11,101,2016-05-05 09:07:12
35,102,2016-05-05 11:07:12
22,103,2016-05-05 12:59:12
77,104,2016-05-05 18:04:12
99,105,2016-05-05 20:36:39

hadoop fs -mkdir /tmp/zxm/articles
hadoop fs -mkdir /tmp/zxm/articles/user_actions

select * from user_actions;

select user_id, collect_set(article_id) from user_actions group by user_id;
select user_id, collect_list(article_id) from user_actions group by user_id;

drop table if exists user_actions;


==================== article theme ====================
article_id, article_url, key_words

101,http://abcn.net/,kw8|kw1
102,http://www.abcn.net/,kw6|kw3
103,http://dfeas.de/,kw7
104,http://asdf.fr/,kw5|kw1|kw4|kw9
105,http://34ad5.eu/,

hadoop fs -mkdir /tmp/zxm/articles/article_kws
hadoop fs -put article_kws.txt /tmp/zxm/articles/article_kws/

drop table if exists articles;

CREATE EXTERNAL TABLE articles (
    article_id STRING,
    url STRING,
    kws array<STRING>
)

ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '|'
LOCATION '/tmp/zxm/articles/article_kws';

select * from articles;

select article_id,kw
from articles
lateral view explode(kws) t as kw;

select article_id,kw
from articles
lateral view outer explode(kws) t as kw;

select a.user_id, b.kw
from user_actions as a
left outer join (
    select article_id, kw
    from articles
    LATERAL VIEW OUTER explode(kws) t AS kw
) b
on (a.article_id = b.article_id)
order by a.user_id;

select a.user_id, b.kw,count(1) as weight
from user_actions as a
left outer join (
    select article_id, kw
    from articles
    LATERAL VIEW OUTER explode(kws) t AS kw
) b
on (a.article_id = b.article_id)
group by a.user_id,b.kw
order by a.uesr_id, weight desc;

-- 把每个keyword, value对拼成一个key:value样式字符串
select a.user_id, concat_ws(':', b.kw, cast (count(1) as string)) as kw_w
from user_actions as a
left outer join (
    select article_id, kw
    from articles
    LATERAL VIEW OUTER explode(kws) t AS kw
) b
on (a.article_id = b.article_id)
group by a.user_id, b.kw;

11      kw1:4
11      kw4:1
11      kw5:1


-- 拼凑map样式字符串

select cc.user_id, concat_ws(",", collect_set(cc.kw_w))
from (
    select a.user_id, concat_ws(':', b.kw, cast (count(1) as string)) as kw_w
    from user_actions as a
    left outer join (
        select article_id, kw
        from articles
        LATERAL VIEW OUTER explode(kws) t AS kw
    ) b
    on (a.article_id = b.article_id)
    group by a.user_id, b.kw
) as cc
group by cc.user_id

11      kw1:4,kw4:1,kw5:1,kw8:3,kw9:1
22      kw1:1,kw3:1,kw4:1,kw5:1,kw6:1,kw7:2,kw9:1

-- 用str_to_map转换成map

select cc.user_id, str_to_map(concat_ws(",", collect_set(cc.kw_w))) as wm
from (
    select a.user_id, concat_ws(':', b.kw, cast (count(1) as string)) as kw_w
    from user_actions as a
    left outer join (
        select article_id, kw
        from articles
        LATERAL VIEW OUTER explode(kws) t AS kw
    ) b
    on (a.article_id = b.article_id)
    group by a.user_id, b.kw
) as cc
group by cc.user_id

-- 最终放到一个表里
create table user_kws as
select cc.user_id, str_to_map(concat_ws(",", collect_set(cc.kw_w))) as wm
from (
    select a.user_id, concat_ws(':', b.kw, cast (count(1) as string)) as kw_w
    from user_actions as a
    left outer join (
        select article_id, kw
        from articles
        LATERAL VIEW OUTER explode(kws) t AS kw
    ) b
    on (a.article_id = b.article_id)
    group by a.user_id, b.kw
) as cc
group by cc.user_id

hive> select user_id, wm['kw1'] from user_kws;
OK
11      4
22      1
33      1

提取map字段的keys, values分别作为列表返回

select user_id, map_keys(wm), map_values(wm)
 from user_kws;


用lateral view 打开，只不过打开成一个视图后，里面有两个值，key和value
select user_id, keyword, weight
from user_kws
lateral view explode(wm) t as keyword, weight;
