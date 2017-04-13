# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import Queue
from proxy_pool import ProxyFactory
import multiprocessing

#### set your own case number
my_num = 'YSC1790114991'
my_num = long(my_num[3:])

### the range before and after you want to search
search_range = 200

##### maximum time to sleep
max_sleep_time = 5

##### process number
process_num = 4

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
              'Notice Was Returned To USCIS Because The Post Office Could Not Deliver It' : 'Returned',
              'Card Was Mailed To Me' : 'Card Mailed',
              'New Card Is Being Produced' : 'Card Produced',
              'Case Rejected Because I Sent An Incorrect Fee' : 'Rejected Incorrect Fee'
              }

proxy_pool = []

def sleep_random_time():
    time.sleep(random.randint(0, max_sleep_time))

def get_res_one_case(num, process_id):
    post_data['appReceiptNum'] = num
    try:
        proxy_addr = get_random_proxy_addr()
        # proxy_addr = 'http://159.203.123.37:3128'
        proxies = {"http" : proxy_addr}
        r = requests.post(uscis_url, data=post_data, headers=headers, proxies = proxies)
        soup = BeautifulSoup(r.content)
        res = soup.form.h1.string
        cur_res = soup.form.p.contents[0]
    except:
        print 'In process {0}, cannot process case: '.format(process_id) + num
        return False

    print 'In process %d, '%(process_id) + num + ': ' + res
    if res in res2status:
        if process_id < process_num and all_res_before.qsize() < search_range:
            all_res_before.put(num + ': ' + res)
        if process_id >= process_num and all_res_after.qsize() < search_range:
            all_res_after.put(num + ': ' + res)

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

class GetOptProcess(multiprocessing.Process):
    def __init__(self, process_id, start_num, end_num, order):
        multiprocessing.Process.__init__(self)
        self.process_id = process_id
        self.start_num = start_num
        self.end_num = end_num
        self.order = order

    def run(self):
        for num in range(self.start_num, self.end_num, self.order):
            if self.process_id < process_num and all_res_before.qsize() >= search_range:
                return
            if self.process_id >= process_num and all_res_after.qsize() >= search_range:
                return
            sleep_random_time()
            get_res_one_case('YSC'+str(num), self.process_id)

def get_opt_res():
    global all_res_after
    global all_res_before
    manager = multiprocessing.Manager()
    all_res_before = manager.Queue()
    all_res_after = manager.Queue()
    all_process = []
    total = search_range + search_range / 10
    num = (total + process_num - 1) / process_num
    start_num = my_num - 1;
    for i in range(process_num):
        cur_process = GetOptProcess(i, start_num, start_num - num, -1)
        cur_process.start()
        all_process.append(cur_process)
        start_num -= num

    start_num = my_num + 1;
    for i in range(process_num):
        cur_process = GetOptProcess(process_num + i, start_num, start_num + num , 1)
        cur_process.start()
        all_process.append(cur_process)
        start_num += num

    for process in all_process:
        process.join()

    with open('num.txt', 'w') as f:
        while not all_res_before.empty():
            f.write(all_res_before.get() + '\n')
        while not all_res_after.empty():
            f.write(all_res_after.get() + '\n')

def get_proxy_pool():
    pf = ProxyFactory()
    pf.Run()
    global proxy_pool
    proxy_pool = pf.proxyPairs
    # print proxy_pool

def get_random_proxy_addr():
    index = random.randint(0, len(proxy_pool))
    return proxy_pool[index][0]

def main():
    get_proxy_pool()
    get_opt_res()
    process_opt_res()

if __name__ == '__main__':
    main()
