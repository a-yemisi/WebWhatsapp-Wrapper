import new_messages_observer
import os
from fastapi import FastAPI, Path, Body, BackgroundTasks

from webwhatsapi import WhatsAPIDriver
app = FastAPI()


def startsession():
    os.environ["SELENIUM"] = "http://seleniumHub-openWa-ii:4444/wd/hub"
    global driver
    driver = WhatsAPIDriver(client='chrome-remote', command_executor=os.environ["SELENIUM"])
    print("Waiting for QR")
    driver.wait_for_login()
    print("Bot started")


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
        return{"Error": "Session could not start"}

@app.post("/v1/api/send-whatsapp-message/")
def send_whatsapp_message(mobile_number: str= Body(...), message: str= Body(...)):
    try:
        driver.send_message_via_selenium(mobile_number, message)
        return{"Success": "Message sent successfully!"}
    except Exception as e:
        print("Error:", e)
        return{"Error": "Message not sent"}

    
@app.get("/v1/api/kill-session/")
def kill_whatsapp_session():
    try:
        driver.quit()
        return{"Session killed successfully"}
    except Exception as e:
        print("Error:", e)
        return{"Error killing session"}
