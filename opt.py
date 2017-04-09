# -*- coding: utf-8 -*-

import requests
import os
import sys
import re
from bs4 import BeautifulSoup
import time
import random
import threading
import Queue

#### set your own case number without letters
my_num = 'YSC1790114991'
my_num = long(my_num[3:])

### the range before and after you want to search
search_range = 5

##### maximum time to sleep
max_sleep_time = 0

########### For HTTP request ###############
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
uscis_url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
### data for POST
post_data = {
    'appReceiptNum' : 'YSC1790114991',
    'initCaseSearch' : 'CHECK STATUS'
}
########### For HTTP request ###############

##### output file
f1 = open("num.txt", "w")

### dic to save all the results and abbreviations
res2status = {'Case Was Received' : 'Received',
              'Case Was Approved' : 'Approved',
              'Request for Initial Evidence Was Mailed' : 'Request',
              'Correspondence Was Received And USCIS Is Reviewing It' : 'Review',
              'Decision Notice Mailed' : 'Denied',
              'Notice Was Returned To USCIS Because The Post Office Could Not Deliver It' : 'Returned'
}

def sleep_random_time():
    time.sleep(random.randint(0, max_sleep_time))

def get_res_one_case(num):
    post_data['appReceiptNum'] = num
    sleep_random_time()
    r = requests.post(uscis_url, data=post_data, headers=headers)
    soup = BeautifulSoup(r.content)
    res = soup.form.h1.string
    all_res = soup.form.p.contents[0]
    if all_res.find('I-765') > -1:
        print num, ': ' + res
        f1.write(num + ": " + res + '\n')
        return True
    else:
        return False

def get_opt_res():
    before_count, after_count = 0, 0
    before, after = my_num, my_num
    while True:
        if before_count < search_range:
            before -= 1
            if get_res_one_case('YSC'+str(before)):
                before_count += 1
        if after_count < search_range:
            after += 1
            if get_res_one_case('YSC'+str(after)):
                after_count += 1
        if after_count >= search_range and before_count >= search_range:
            break;
    f1.close()

def get_res_from_file(filename):
    with open(filename, "r") as f1:
        lines = f1.readlines()
        res = {}
        for line in lines:
            res[line.split(':')[0].strip()] = line.split(':')[1].strip()
        return res

def process_opt_res():
    pre = get_res_from_file('num.txt')
    res= {}
    for v in res2status.values():
        res[v] = [0, 0] #count before and after, respectively.
    for k, v in pre.items():
        if int(k[3:]) <= my_num and v in res2status:
            res[res2status[v]][0] += 1
        if int(k[3:]) > my_num and v in res2status:
            res[res2status[v]][1] += 1
    total_before, total_after = 0, 0
    for v in res.values():
        total_before += v[0]
        total_after += v[1]
    print 'Final Results: '
    print '#########################'
    for k in sorted(res.keys()):
        print 'Before me '+k+': %d/%d ' % (res[k][0], total_before)
    print '#########################'
    for k in sorted(res.keys()):
        print 'After me '+k+': %d/%d ' % (res[k][1], total_after)
    print '#########################'

def main():
    get_opt_res()
    process_opt_res()

if __name__ == '__main__':
    main()
