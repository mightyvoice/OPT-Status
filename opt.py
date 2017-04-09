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

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

uscis_url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

### data for POST
post_data = {
    'appReceiptNum' : 'YSC1790114991',
    'initCaseSearch' : 'CHECK STATUS'
}

##### output file
f1 = open("num.txt", "w")

#### set your own case number without letters
my_num = 1790114991

### the range before and after you want to search
search_range = 2000

### dic to save all the results and abbreviations
res2status = {'Case Was Received' : 'Received',
              'Case Was Approved' : 'Approved',
              'Request for Initial Evidence Was Mailed' : 'Request',
              'Correspondence Was Received And USCIS Is Reviewing It' : 'Review',
              'Decision Notice Mailed' : 'Denied',
              'Notice Was Returned To USCIS Because The Post Office Could Not Deliver It' : 'Returned'
}

def sleep_random_time():
    time.sleep(random.randint(1, 5))

def get_opt_num():
    with open("res.txt", "r") as f1:
        lines = f1.readlines()
        res = {}
        for line in lines:
            res[line.split(':')[0].strip()] = line.split(':')[1].strip()
        return res

def get_opt_res():
    nums = sorted(get_opt_num().keys())
    for num in nums:
        post_data['appReceiptNum'] = num
        r = requests.post(uscis_url, data=post_data, headers=headers)
        soup = BeautifulSoup(r.content)
        res = soup.form.h1.string
        all_res = soup.form.p.contents[0]
        if all_res.find('I-765') > -1:
            print num, ': '+res
            f1.write(num + ": " + res + '\n')
        sleep_random_time()
    f1.close()

def process_pot_res():
    pre = get_opt_num()
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
    for k, v in res.items():
        print 'Before me '+k+': %d/%d ' % (v[0], total_before)
    for k, v in res.items():
        print 'After me '+k+': %d/%d ' % (v[1], total_after)

def main():
    process_pot_res()

if __name__ == '__main__':
    main()
