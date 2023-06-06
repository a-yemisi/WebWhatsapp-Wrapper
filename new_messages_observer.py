import os, re
import sys
import time
import requests
import json

from webwhatsapi import WhatsAPIDriver


def run(driver):
    # print("Environment", os.environ)
    # try:
    #     os.environ["SELENIUM"] = "http://127.0.0.1:4449/wd/hub"
    # except KeyError:
    #     print("Please set the environment variable SELENIUM to Selenium URL")
    #     sys.exit(1)

    # driver = WhatsAPIDriver(client="chrome", command_executor=os.environ["SELENIUM"])
    # print("Waiting for QR")
    # try:
    #     driver.wait_for_login()
    #     print("Bot started")
    # except Exception as e:
    #     print("Error:", e)
    #     driver.quit

    driver.subscribe_new_messages(NewMessageObserver())
    print("Waiting for new messages...")

    """ Locks the main thread while the subscription in running """
    while True:
        # time.sleep(60)
        try:
            message_received = driver.return_received_message()
            if len(message_received) == 0:
                # print("Not receiving message")
                pass
            else:
                try:
                    for i in message_received:
                        message_content, sender_id = i
                        print("Message Received: '{}' received from  {}".format(message_content, sender_id))
                        driver.chat_send_seen(sender_id)
                        mobile = re.sub(r'\D', '', sender_id)
                        try:
                            url = "https://sociallenderng.com/apisl/v3/callbacks/whatsappwebapi"
                            payload = json.dumps({
                                "phone": mobile,
                                "body": message_content
                            })
                            headers = {
                            'Content-Type': 'application/json',
                            'Cookie': 'PHPSESSID=0428102fe34ab5c591d05adf483f2db4'
                            }
                            requests.request("GET", url, headers=headers, data=payload)
                        except Exception as e:
                            pass
                        
                        message_received.clear()
                    # return mobile_number, message_content
                except:
                    pass
        except Exception as e:
                print("Error:", e)
                # driver.quit()
                # run_observe_message(driver)




class NewMessageObserver:
    def on_message_received(self, new_messages):
        for message in new_messages:
            if message.type == "chat":
                return message.content, message.sender.id
            else:
                pass
