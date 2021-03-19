# read README.txt for further details
# Wow, Anon, Corporate America is really getting out of hand...
# But it's not like I'd ever be enslaved to buy the next product :^)
# *braaaaaaaaaaaaaaaaap* *sniff sniff*
# What's this, my dear? The next gaming console by Microjeet!?
# It's going to have Halo produced by a disappointing studio!?
# A-anon, I m-m-must COOOOOOOOOOOOOOOOMSUUUUUUME

import requests
import json
import time
import smtplib, ssl
import tweepy
import traceback
import os
from twilio.rest import Client
from datetime import datetime

# Twitter API data
TWITTER_CONSUMER_KEY = 'CONSUMER_KEY'
TWITTER_CONSUMER_SECRET = 'CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN = 'ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

# Email data
EMAIL_SENDER = 'SENDER_EMAIL_ADDRESS'
EMAIL_PASSWORD = 'SENDER_PASSWORD'
EMAIL_RECEIVER = 'RECEIVER_EMAIL_ADDRESS'
SMTP_SERVER = 'smtp.gmail.com' # email server you're using to send
PORT = 465 # email server port

# Twilio text data
TWILIO_SID = 'SID' # your Twilio SID
TWILIO_TOKEN = 'AUTHENTICATION_TOKEN' # your Twilio authentication token
SENDER_PHONE = '+15551234567' # your Twilio phone number
RECEIVER_PHONE = '+15551234567' # phone number you want to text

green_light = u'\U0001F7E2' # For Twitter emoji
red_light = u'\U0001F534' # For Twitter emoji
checkered_flag = (u'\U0001F3C1') # For Twitter emoji
red_flag = (u'\U0001F6A9') # For Twitter emoji
offline = f'Bot Status: {red_light} Offline'
out_of_stock = (f'Bot Status: {green_light} Online | Stock: '
           f'{red_light} Out of Stock')
in_stock = (f'Bot Status: {green_light} Online | Stock: '
           f'{green_light} In Stock')

current_template = {"9000000013": False, "0059": False, "0075": False,
                    "0064": False, "0037": False, "0031": False}
previous_template = {"9000000013": False, "0059": False, "0075": False,
                     "0064": False, "0037": False, "0031": False}


def sendTweet(message, set_status=False):
    '''Sends tweets and updates account name'''

    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        if set_status:
            name = message
            api.update_profile(name)
        if not set_status:
            api.update_status(message)
    except:
        error_alert = f'Failed to send tweet: "{message}"!'
        trace_log = traceback.print_exc()
        # Only prints when it errors with no crash to save disk space
        print(f'{trace_log}\n{error_alert}')


def sendEmail(message):
    '''Sends emails when errors occur'''

    email_text = f'Subject: Message from server!\n{message}'
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_text)
    except:
        error_alert = f'Failed to send Email: "{message}"!'
        trace_log = traceback.print_exc()
        print(f'{trace_log}\n{error_alert}')


def sendText(message):
    '''Sends texts when errors occur'''

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    try:
        client.messages.create(to = RECEIVER_PHONE,
                               from_ = SENDER_PHONE,
                               body = message)
    except:
        error_alert = f'Failed to send Text: "{message}"!'
        trace_log = traceback.print_exc()
        print(f'{trace_log}\n{error_alert}')


def stockReader(js):
    '''Parses the json returned by the GET request in checkStock()'''

    store_dict = {'Microsoft': '9000000013',
                'Best Buy': '0059',
                'GameStop': '0075',
                'Target': '0064',
                'Walmart': '0037',
                'AntOnline': '0031'}
    available_list = []
    unavailable_list = []
    current_state_js = {}
    # Safely open stock state json files
    with open('current_stock_state.json', 'r+') as current_state, open(('previo'
              'us_stock_state.json'), 'r+') as previous_state:
        current_state_js = json.load(current_state)
        previous_state_js = json.load(previous_state)
        try:
            for key, value in store_dict.items():
                if (js['availableLots']['0001-01-01T00:00:00.0000000Z']
                    [value]['inStock'] == 'True'):
                    current_state_js[value] = True
                    # Only append keys to list if stock state has changed
                    # This is what prevents duplicate stock alerts
                    if current_state_js[value] != previous_state_js[value]:
                        available_list.append(key)
                        previous_state_js[value] = True
                if (js['availableLots']['0001-01-01T00:00:00.0000000Z']
                    [value]['inStock'] == 'False'):
                    current_state_js[value] = False
                    if current_state_js[value] != previous_state_js[value]:
                        unavailable_list.append(key)
                        previous_state_js[value] = False
            if available_list:
                sendTweet(in_stock, set_status=True)
            if unavailable_list:
                if all(value==False for value in current_state_js.values()):
                    message = (f'Bot Status: {green_light} Online | Stock: '
                               f'{red_light} Out of Stock')
                    sendTweet(message, set_status=True)
        except:
            js_alert = f'JSON: {js}'
            error_alert = 'Script encountered a fatal error while parsing JSON!'
            trace_log = traceback.print_exc()
            log_data = f'{trace_log}\n{js_alert}\n{error_alert}'
            sendTweet(offline, set_status=True)
            sendText(error_alert)
            sendEmail(error_alert)
            print(log_data)
            raise Exception(error_alert)
        # Safely overwrite stock state json files
        current_state.seek(0)
        json.dump(current_state_js, current_state)
        current_state.truncate()
        previous_state.seek(0)
        json.dump(previous_state_js, previous_state)
        previous_state.truncate()
    return available_list, unavailable_list, current_state_js


def checkStock():
    '''Requests stock & passes appropriate args for message. Returns boolean'''

    url = ('https://inv.mp.microsoft.com/v2.0/inventory/US/8WJ714N3RBTL/490G/'
           '8WFTS4MLK3L9')
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78'
               '.0) Gecko/20100101 Firefox/78.0'),
               'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate',
               'Origin': 'https://www.xbox.com',
               'Connection': 'keep-alive',
               'Referer': 'https://www.xbox.com/en-US/consoles/xbox-series-x',
               'TE': 'Trailers'}
    resp = requests.get(url, headers)
    if 'json' in resp.headers.get('Content-Type'):
        js = resp.json()
        available_list, unavailable_list, current_state_js = stockReader(js)
        if available_list: # now in stock
            available_list = formatGrammar(available_list)
            message = (f'{checkered_flag} #XboxSeriesX is currently in stock at'
                      f' {available_list}!')
            sendTweet(message)
        if unavailable_list: # now out of stock
            unavailable_list = formatGrammar(unavailable_list)
            message = (f'{red_flag} #XboxSeriesX is now out of stock at'
                      f' {unavailable_list}!')
            sendTweet(message)
        for value in current_state_js.values():
            if value == True:
                return True # In stock
        return False # Out of stock
    else:
        status_alert = f'Response Status Code: {resp.status_code}'
        head_alert = f'Response Headers: {resp.headers}'
        error_alert = 'Script encountered a fatal error while requesting JSON!'
        trace_log = traceback.print_exc()
        log_data = f'{trace_log}\n{status_alert}\n{head_alert}\n{error_alert}'
        sendTweet(offline, set_status=True)
        sendText(error_alert)
        sendEmail(error_alert)
        print(log_data)
        raise Exception(error_alert)


def formatGrammar(list):
    '''Grammatically formats available_list & unavailable_list for messaging'''

    # Formats list with appropriate commas & "and" if the list length is > 2
    if len(list) > 2:
        last_item = f', and {list.pop()}'
        list = ', '.join(list)
        list += last_item
    # Formats list with "and" if the list length is 2
    elif len(list) == 2:
        last_item = f' and {list.pop()}'
        list = list.pop()
        list += last_item
    # Does no formatting if the list length is less than two
    else:
        list = list.pop()
    return list


def writeToLog(data):
    '''Writes data to a log file'''

    with open('coomsumer.log', 'w') as script_log:
        script_log.seek(0)
        script_log.write(data)


# Creates stock state files and populates them if non-existent
if not os.path.isfile('current_stock_state.json'):
    with open('current_stock_state.json', 'w') as current_state:
        json.dump(current_template, current_state)
if not os.path.isfile('previous_stock_state.json'):
    with open('previous_stock_state.json', 'w') as previous_state:
        json.dump(previous_template, previous_state)
# Starts script with correct bot and stock status
with open('current_stock_state.json', 'r') as current_state:
    current_state_js = json.load(current_state)
    if True in current_state_js.values():
        sendTweet(in_stock, set_status=True)
    else:
        sendTweet(out_of_stock, set_status=True)
# Checks stock every 420 milliseconds
attempts = 0
while True:
    time.sleep(0.420)
    attempts += 1
    attempt = f'Attempt: {attempts}'
    if checkStock():
        current_time = datetime.now().strftime('%b-%d-%Y %I:%M:%S %p')
        message = f'Stock: In Stock\nTimestamp: {current_time}'
        data = f'{attempt}\n{message}\n'
        writeToLog(data)
    else:
        current_time = datetime.now().strftime('%b-%d-%Y %I:%M:%S %p')
        message = f'Stock: Out of Stock\nTimestamp: {current_time}'
        data = f'{attempt}\n{message}\n'
        writeToLog(data)
