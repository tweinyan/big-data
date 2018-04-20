from itertools import groupby
from operator import itemgetter
import sys

def read_line(file):
    for line in file:
        line = line.strip()
        if line == '':
            continue
        fields = line.split('\t')
        yield fields

def main():
    data_iter = read_line(sys.stdin)
    print(groupby(data_iter, itemgetter(0)))
    #for i in groupby(data_iter, itemgetter(0)):
    #    print(i)

    #for key, kviter in groupby(data_iter, itemgetter(0)):
    #    user_id = key
    #    user_loc = None
    #    order_cnt = 0
    #    order_sum = 0
    #    for line in kviter:
    #        fields = line[1].split(':')
    #        if len(fields) == 2:
    #            user_loc = fields[1]
    #        elif len(fields) == 3:
    #            order_cnt += 1
    #            order_sum += int(fields[2])
    #    print('{0}\t{1}:{2}:{3}'.format(user_id, user_loc, order_cnt, order_sum))

if __name__ == '__main__':
    main()
