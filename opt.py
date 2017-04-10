# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import threading
import Queue

#### set your own case number without letters
my_num = 'YSC1790114991'
my_num = long(my_num[3:])

### the range before and after you want to search
search_range = 100

##### maximum time to sleep
max_sleep_time = 5

##### thread number
thread_num = 5

## output file name
output_file = 'num.txt'

########### For HTTP request ###############
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
uscis_url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
### data for POST
post_data = {
    'appReceiptNum' : 'YSC1790114991',
    'initCaseSearch' : 'CHECK STATUS'
}
########### For HTTP request ###############

#### store all the results
all_res_before = Queue.Queue()
all_res_after = Queue.Queue()

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

def get_res_one_case(num, thread_id):
    post_data['appReceiptNum'] = num
    sleep_random_time()
    r = requests.post(uscis_url, data=post_data, headers=headers)
    print r.status_code
    if r.status_code != 200:
        print 'Cannot connect to the website'
        exit(0)
    soup = BeautifulSoup(r.content)
    res = soup.form.h1.string
    cur_res = soup.form.p.contents[0]
    if cur_res.find('I-765') > -1:
        print 'In thread %d, '%(thread_id) + num + ': ' + res
        if thread_id < thread_num:
            if all_res_before.qsize() < search_range:
                all_res_before.put(num + ': ' + res)
        else:
            if all_res_after.qsize() < search_range:
                all_res_after.put(num + ': ' + res)
        return True
    else:
        return False

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
        if int(k[3:]) < my_num and v in res2status:
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

class GetOptThread(threading.Thread):
    def __init__(self, thread_id, start_num, end_num, order):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.start_num = start_num
        self.end_num = end_num
        self.order = order

    def run(self):
        for num in range(self.start_num, self.end_num, self.order):
            if self.thread_id < thread_num and all_res_before.qsize() >= search_range:
                break;
            if self.thread_id >= thread_num and all_res_after.qsize() >= search_range:
                break;
            get_res_one_case('YSC'+str(num), self.thread_id)

def get_opt_res():
    all_threads = []
    total = search_range * 10;
    num = (total + thread_num - 1) / thread_num
    start_num = my_num - 1;
    for i in range(thread_num):
        cur_thread = GetOptThread(i, start_num, start_num - num, -1)
        cur_thread.start()
        all_threads.append(cur_thread)
        start_num -= num

    start_num = my_num + 1;
    for i in range(thread_num):
        cur_thread = GetOptThread(thread_num + i, start_num, start_num + num, 1)
        cur_thread.start()
        all_threads.append(cur_thread)
        start_num += num

    for thread in all_threads:
        thread.join()

    with open('num.txt', 'w') as f:
        while not all_res_before.empty():
            f.write(all_res_before.get() + '\n')
        while not all_res_after.empty():
            f.write(all_res_after.get() + '\n')

def main():
    get_opt_res()
    process_opt_res()

if __name__ == '__main__':
    main()
