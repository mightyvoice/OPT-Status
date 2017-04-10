
# What to do
Look up a certain number of OPT application status before and after yours.

The final statistc will be shown in the terminal like this:
***
Before me Received: 187/425     
Before me Returned: 2/425        
Before me Review: 2/425      
Before me Request: 39/425     
Before me Denied: 12/425     
Before me Approved: 183/425      
After me Received: 205/449     
After me Returned: 9/449    
After me Review: 0/449     
After me Request: 29/449     
After me Denied: 17/449     
After me Approved: 189/449 
***

# How to use

## Required python evironment and package
* Python 2.7
* [Request](http://docs.python-requests.org/en/master/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## How to run

* Change the **my_num** variable in opt.py to your own case number. 
* Change the **search_range** variable in opt.py to the number of cases you want to query before and after your own. The default number is 200.
* Just run the following command in the terminal:  
**python opt.py**
* All the results will write to the file: **num.txt**.
