import new_messages_observer
import os
from typing import List
from fastapi import FastAPI, Path, Body, BackgroundTasks
from fastapi.exceptions import HTTPException

from webwhatsapi import WhatsAPIDriver
app = FastAPI()


def startsession():
    # os.environ["SELENIUM"] = "http://seleniumHub-openWa-ii:4444/wd/hub"
    os.environ["SELENIUM"] = "http://40.117.178.47/:4444/wd/hub"
    global driver
    driver = WhatsAPIDriver(client='chrome-remote', command_executor=os.environ["SELENIUM"])
    print("Waiting for QR")
    # driver.wait_for_login()
    # print("Bot started")


# Run receive message
# new_messages_observer.run_observe_message(driver)
@app.get("/v1/api/startsession/")
def start_whatsapp_session(background_task: BackgroundTasks):
    try:
        startsession()
        background_task.add_task(new_messages_observer.run, driver)
        return{"Success":"Session started"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/v1/api/send-whatsapp-message/")
def send_whatsapp_message(mobile_number: int= Body(...), message: str= Body(...)):
    try:
        str_mobile_number = str(mobile_number)
        number_id = str_mobile_number + '@c.us'
        print("Number to be sent to:", number_id)
        driver.chat_send_message(number_id, message)
        return{"Success": "Message sent successfully!"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/v1/api/send-bulk-whatsapp-message/")
def send_bulk_whatsapp_message(mobile_numbers: List[int]= Body(...), messages: str= Body(...)):
    try:
        for number in mobile_numbers:
            str_number = str(number)
            str_number = str_number + '@c.us'
            print("Number to be sent to:", str_number)
            driver.chat_send_message(str_number, messages)
            print("Sent")
        return{"Success": "Messages sent successfully!"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
            

@app.get("/v1/api/kill-session/")
def kill_whatsapp_session():
    try:
        driver.quit()
        return{"Session killed successfully"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
