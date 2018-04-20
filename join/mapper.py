#!/usr/bin/python
# encoding: utf-8

import sys

def main():
    for line in sys.stdin:
        user_id = None
        product_id = None
        user_loc = None
        order_id = None
        source = None
        line = line.strip()
        if line == "":
            continue
        fields = line.split('\t')
        if len(fields) == 3:
            # user data
            source = 'A'
            user_id, _, user_loc = fields
            print('{0}\t{1}:{2}'.format(user_id, source, user_loc))

        elif len(fields) == 4:
            source = 'B'
            order_id, user_id, product_id, price = fields
            print('{0}\t{1}:{2}:{3}'.format(user_id, source, order_id, price))

if __name__ == '__main__':
    main()
