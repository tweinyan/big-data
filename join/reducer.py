#!/usr/bin/python
# encoding: utf-8
"""
输出：
cat data/*|python mapper.py |sort -k1,2 | python reducer.py
1       BJ
2       BJ
2       BJ
3       BJ
3       TJ
"""

import sys

last_user_id = None
cur_loc = '-'
order_cnt = 0
price_sum = 0

for line in sys.stdin:
    line = line.strip()
    user_id, info = line.split('\t')
    fields = info.split(':')
    if not last_user_id:
        last_user_id = user_id
        cur_loc = fields[1]
        order_cnt = 0
        price_sum = 0
    elif user_id == last_user_id:
        order_cnt += 1
        price_sum += int(fields[2])

    else:
        # a new user
        print('{0}\t{1}:{2}'.format(last_user_id, order_cnt, price_sum))
        last_user_id = user_id
        order_cnt = 0
        price_sum = 0
