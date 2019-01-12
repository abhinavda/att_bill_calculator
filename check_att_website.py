from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time,sys
import calulating_cost

username=sys.argv[1]
userpassword=sys.argv[2]
account_owner=sys.argv[3]

## Intialize
insurance_overall_cost=32.99

broswer_url="https://www.att.com/my/#/viewBill"
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(broswer_url)
time.sleep(10)

## typing the username and password
browser.find_element_by_xpath('//*[@id="userName"]').send_keys(str(username))
browser.find_element_by_xpath('//*[@id="password"]').send_keys(str(userpassword))
browser.find_element_by_xpath('//*[@id="loginButton-lgwgLoginButton"]').click()

## clicks the options, returns false if option is unavailable
def click_options(xpath_element) :
    try :
        browser.find_element_by_xpath(xpath_element).click()
        time.sleep(3)
        return True
    except :
        return False

## keys won't be avaiable until page loads fully. This function checks in intervals to see the page is loaded
def status_check_and_retry(fun_to_call) :
    count = 1
    time.sleep(count)
    click_options('//*[@id="popup-btn-close"]/i') ## Closing popups if they exist
    click_options('//*[@id="fsrInvite"]/section[3]/button[2]') ## Closing popups if they exist
    if fun_to_call==False and count < 9 :
        fun_to_call
        count+=1
    else :
        if count >= 9:
            print "couldn't find the function"
        print "found it"

def check_popup():
    try :
        status_check_and_retry(click_options('//*[@id="fsrInvite"]/section[3]/button[2]'))
        #browser.find_element_by_xpath('//*[@id="fsrInvite"]/section[3]/button[2]').click()
        return True
    except :
        return False

# click billing option
status_check_and_retry(click_options('//*[@id="myBilling"]/div[2]/a'))

# click wireless_option
status_check_and_retry(click_options('//*[@id="tab1"]/div[1]/div/i'))

# Getting all results from page
res=status_check_and_retry(click_options('//*[@id="printfas1"]'))
res=res.text
results_page=res.split('\n') ## gives a list

extra_charge=calulating_cost.internet_charges_per_person(results_page,insurance_overall_cost)
mobile_charges=calulating_cost.calc_price_each_person_mobile(results_page[4:])
final_charges_per_user=calulating_cost.calc_amount_owed(mobile_charges,extra_charge,account_owner)
print final_charges_per_user
print sum(final_charges_per_user.values())
