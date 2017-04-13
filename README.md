
# What to do
Look up a certain number of OPT application status before and after yours.

Using proxy IP address to avoid blocked by the website.

I use [Proxy Pool](https://github.com/mightyvoice/Proxy-Pool) to get available IP addresses.

The final statistc will be shown in the terminal like this:
***
Final Results:   
#########################   
Before me Approved: 5/200   
Before me Card Mailed: 138/200   
Before me Card Produced: 28/200   
Before me Denied: 1/200   
Before me Received: 20/200   
Before me Rejected Incorrect Fee: 0/200   
Before me Request: 4/200   
Before me Returned: 4/200   
Before me Review: 0/200   
#########################   
After me Approved: 1/200   
After me Card Mailed: 100/200   
After me Card Produced: 30/200   
After me Denied: 3/200   
After me Received: 48/200   
After me Rejected Incorrect Fee: 8/200   
After me Request: 7/200   
After me Returned: 3/200   
After me Review: 0/200   
#########################   
***

# How to use

## Required python evironment and package
* Python 2.7
* [Request](http://docs.python-requests.org/en/master/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [PhantomJS](http://phantomjs.org/)
* [Selenium](http://selenium-python.readthedocs.io/)

## How to run

* After installing PhantomJS, change the **PhantomJS_Dir** to your own directory in the proxy_pool.py file.
* Change the **my_num** variable in opt.py to your own case number. 
* Change the **search_range** variable in opt.py to the number of cases you want to query before and after your own. The default number is 20.
* Just run the following command in the terminal:  
**python opt.py**
* All the results will write to the file: **num.txt**.
