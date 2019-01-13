from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time,sys
import calulating_cost

username=sys.argv[1]
userpassword=sys.argv[2]
account_owner=sys.argv[3:] ## Full name should be given. First name followed by last name. Example : Abhinav Damarapati. This was extra charges are remove from main account

## Intialize
insurance_overall_cost=34.99

broswer_url="https://www.att.com/my/#/viewBill"
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(broswer_url)
time.sleep(12)
try:
    ## typing the username and password
    browser.find_element_by_xpath('//*[@id="userName"]').send_keys(str(username))
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(str(userpassword))
    browser.find_element_by_xpath('//*[@id="loginButton-lgwgLoginButton"]').click()
except :
    print "unable to open ATT page"

## clicks the options, returns false if option is unavailable
def click_options(xpath_element) :
    try :
        browser.find_element_by_xpath(xpath_element).click()
        return True
    except :
        return False

def close_popups() :
    try:
        click_options('//*[@id="popup-btn-close"]/i')  ## Closing popups if they exist
        click_options('//*[@id="fsrInvite"]/section[3]/button[2]')  ## Closing popups if they exist
    except :
        pass

# click billing option
time.sleep(5)
status_billing=click_options('//*[@id="myBilling"]/div[2]/a')
if not status_billing :
    time.sleep(5)
    close_popups()
    click_options('//*[@id="myBilling"]/div[2]/a')

# click wireless_option
time.sleep(5)
status_wireless=click_options('//*[@id="tab1"]/div[1]/div/i')
if not status_wireless :
    time.sleep(5)
    close_popups()
    click_options('//*[@id="tab1"]/div[1]/div/i')

# Getting all results from page
time.sleep(5)
try :
    res=browser.find_element_by_xpath('//*[@id="printfas1"]').text
    results_page=res.split('\n') ## gives a list
except :
    print "failed to get results"
browser.close()
##
if len(results_page) >0 :
    extra_charge=calculating_cost.internet_charges_per_person(results_page,insurance_overall_cost)
    mobile_charges=calculating_cost.calc_price_each_person_mobile(results_page[4:])
    final_charges_per_user=calculating_cost.calc_amount_owed(mobile_charges,extra_charge,str(account_owner).strip().upper(),insurance_overall_cost)
    #print final_charges_per_user
    for key, value in final_charges_per_user.iteritems():
        nam1 = key.split(" ")
        name = nam1[0][0] + nam1[0][1:].lower() + " " + nam1[1][0] + nam1[1][1:].lower()
        print "%s : $%.2f"%(name,value)
    print    
    print "Total : ",sum(final_charges_per_user.values())
