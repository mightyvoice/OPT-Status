
import requests
import time
from selenium import webdriver
import multiprocessing
from multiprocessing import Process, Queue

TEST_WEBSITE = "http://www.google.com"

class Proxy:
    def __init__(self, addr, time):
        self.address = addr
        self.time = time

    def __lt__(self, other):
        return self.time < other.time


class ProxyFactory:
    def __init__(self):
        self.pool = []
        self.proxyPairs = []

    def Run(self):
        proxyList = self.FetchProxies()
        # print(proxyList)
        self.ValidateProxies(proxyList)
        self.pool.sort()
        for i in self.pool:
            self.proxyPairs += [(i.address, i.time)]

    def FetchProxies(self):
        print("fetching proxy list...")
        # u = "http://www.freeproxylists.net/zh/?c=cn&f=1&s=u"
        u = "http://www.freeproxylists.net/us.html"
        driver = webdriver.phantomjs.webdriver.WebDriver(executable_path="/usr/local/bin/phantomjs")
        driver.get(u)
        rows = driver.find_elements_by_css_selector("table > tbody > tr")
        proxies = []
        for i in rows:
            if i.text.find("HTTP") != -1:
                cells = i.text.split()
                proxies += [u"http://{0}:{1}".format(cells[0], cells[1])]
        proxies = proxies[1:]
        print("{0} fetched".format(len(proxies)))
        return proxies

    def CheckProxy(self, address, tests, result):
        for t in tests:
            proxy = {"http": address}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
            try:
                start = time.clock()
                data = requests.get(t, proxies = proxy, headers = headers, timeout = 5)
                end = time.clock()
                print("[Proxy {0}]: OK for {1} in time: {2} s".format(address, t, end - start))
                result.put((address, end - start))
            except Exception as e:
                # print(e)
                print("[Proxy {0}]: not available".format(address))

    def ValidateProxies(self, proxyList):
        maxProc = 5
        tests = [TEST_WEBSITE]
        result = Queue()
        start = time.clock()
        for i in proxyList:
            p = Process(target=self.CheckProxy, args=(i, tests, result))
            p.start()
            if len(multiprocessing.active_children()) > maxProc:
                # print('active_children: ', multiprocessing.active_children())
                p.join()

        while len(multiprocessing.active_children()) > 0:
            time.sleep(3)
        end = time.clock()
        # print("total time for validation:", end - start, "s")

        self.pool = []

        while not result.empty():
            a = result.get()
            self.pool += [Proxy(a[0], a[1])]

        print("{0} validated".format(len(self.pool)))

if __name__ == '__main__':
    pf = ProxyFactory()
    pf.Run()
    print(pf.proxyPairs)