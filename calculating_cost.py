#!/bin/python
## This file calulates the cost owed by each person.

dict={}
#str=""
def calc_price_each_person_mobile(arr1) :
    str=""

    for i in range(len(arr1)) :
        if arr1[i][:4]!="AT&T" : ## Eliminates Wearable header
            if arr1[i][0] !="$" : ## Getting only phone number and user name
                str=str+arr1[i]+" " ## creating key for dictionary
            else :
                if arr1[i-1][0] !="$" : ## eliminating feature att also displays if price has increased for user
                    user_name=str.split(" ")[1:]
                    users=" ".join(user_name).strip()
                    dict[users]=dict.get((users),0)+float(arr1[i][1:]) ## adding values. Some users can have multiple devices
                    str=""
    return dict

def internet_charges_per_person(arr1,insurance) :
    num_users = int(arr1[2].split(" ")[0]) ## Getting the number of users
    #print num_users
    total_cost_for_internet=float(arr1[3][1:]) ## shared price for users
    #print total_cost_for_internet
    internet_charge_per_person=total_cost_for_internet/num_users ## splitting cost for internet
    insurance_cost_per_person=insurance/num_users ## splitting cost for insurance
    return internet_charge_per_person+insurance_cost_per_person


## Just to round off the values
def rounding_values(x):
    return(round(x+0.001,2))

## Modyfing the dictionary mobile_charges
def calc_amount_owed(mobile,extra,main_user,insurance) :
    for i in mobile.keys() :
        if i == main_user: ## main user is charged for insurance. Subtracting the cost from his bill and splitting to everyone.
            mobile[i]=mobile.get(i)-insurance
        mobile[i]=mobile.get(i)+extra
        mobile[i]=rounding_values(mobile.get(i))
    return mobile ## dictionary with final values
