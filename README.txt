Author: An angry neckbeard (with no beard)
Creation Date: Mar-18-2021

Description: 
The Xbox Series X is aids to obtain at retail price due to limited stock. This script sends Twitter alerts whenever Xbox Series X stock becomes available or unavailable at any 1 of 6 retailers.
(Microsoft, Best Buy, GameStop, Target, Walmart, and AntOnline)

Requirements: Twilio and Tweepy libraries:
* pip3 install twilio
* pip3 install tweepy

Notes: 
* Checks stock every 420 milliseconds using a single GET request to a Microsoft server
* Microsoft server returns 2.8kb of data with each request
* Avoids duplicate alerts with stock state checking
* Uses json files for stock states for crash recoveries
* Grammatically formats store lists before tweeting
* Sends a text message and an email when the script encounters an error
* Updates Twitter account name to display the "Bot Status" as "Offline" when an error occurs
* Updates Twitter account name with stock status and tweets out only when the stock state has changed
* Custom prune-enabled logging with writeToLog() is used for my setup to save disk space when redirecting stdout to a log file. Only errors trigger stdout events

*current state of would-be Xbox Series X purchasers*
───────▄▀▀▀▀▀▀▀▀▀▀▄▄
────▄▀▀░░░░░░░░░░░░░▀▄
──▄▀░░░░░░░░░░░░░░░░░░▀▄
──█░░░░░░░░░░░░░░░░░░░░░▀▄
─▐▌░░░░░░░░▄▄▄▄▄▄▄░░░░░░░▐▌
─█░░░░░░░░░░░▄▄▄▄░░▀▀▀▀▀░░█
▐▌░░░░░░░▀▀▀▀░░░░░▀▀▀▀▀░░░▐▌
█░░░░░░░░░▄▄▀▀▀▀▀░░░░▀▀▀▀▄░█
█░░░░░░░░░░░░░░░░▀░░░▐░░░░░▐▌
▐▌░░░░░░░░░▐▀▀██▄░░░░░░▄▄▄░▐▌
─█░░░░░░░░░░░▀▀▀░░░░░░▀▀██░░█
─▐▌░░░░▄░░░░░░░░░░░░░▌░░░░░░█
──▐▌░░▐░░░░░░░░░░░░░░▀▄░░░░░█
───█░░░▌░░░░░░░░▐▀░░░░▄▀░░░▐▌
───▐▌░░▀▄░░░░░░░░▀░▀░▀▀░░░▄▀
───▐▌░░▐▀▄░░░░░░░░░░░░░░░░█
───▐▌░░░▌░▀▄░░░░▀▀▀▀▀▀░░░█
───█░░░▀░░░░▀▄░░░░░░░░░░▄▀
──▐▌░░░░░░░░░░▀▄░░░░░░▄▀
─▄▀░░░▄▀░░░░░░░░▀▀▀▀█▀
▀░░░▄▀░░░░░░░░░░▀░░░▀▀▀▀▄▄▄▄▄