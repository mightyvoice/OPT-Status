
# What to do
Look up a certain number of OPT application status before and after yours.

Using proxy IP address to avoid blocked by the website.

I use [Proxy Pool](https://github.com/mightyvoice/Proxy-Pool) to get available IP addresses.

The final statistc will be shown in the terminal like this:
***
Final Results: 
#########################  
Before me Approved: 5/20   
Before me Denied: 1/20   
Before me Received: 10/20   
Before me Request: 2/20   
Before me Returned: 2/20   
Before me Review: 0/20 
#########################  
After me Approved: 1/20   
After me Denied: 1/20   
After me Received: 13/20   
After me Request: 4/20   
After me Returned: 1/20   
After me Review: 0/20    
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

* Change the **my_num** variable in opt.py to your own case number. 
* Change the **search_range** variable in opt.py to the number of cases you want to query before and after your own. The default number is 20.
* Just run the following command in the terminal:  
**python opt.py**
* All the results will write to the file: **num.txt**.
