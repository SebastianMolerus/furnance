from selenium.webdriver import *
from selenium.webdriver.common.by import By
import json
from time import sleep

paramRequest = "https://www.econet24.com/service/getDeviceParams?uid=AFGPPB0Z32D1P148G02G0&_=1763824107482"
mainPage = "https://www.econet24.com/main/"

def get_device_parameters() -> json:
    chrome.get(paramRequest)
    elem = chrome.find_element(By.TAG_NAME, "pre")
    son = json.loads(elem.text)
    chrome.get(mainPage)
    sleep(10)
    return son

def open_diagram() -> None:
    chrome.find_element(By.ID, "tabHrSchema").click()

def open_main_page() -> None:
    chrome.get(mainPage)
    sleep(10)

def login(user: str, password: str) -> None:
    user_name = chrome.find_element(By.ID, "username")
    user_name.send_keys(user)

    password = chrome.find_element(By.ID, "password")
    password.send_keys(password)

    login_button = chrome.find_element(By.ID, "btnLogin")
    login_button.click()


global chrome 
chrome = Chrome()
chrome.minimize_window()
open_main_page()
login("<>", "<>")

def set_mixer_temp(new_temp : int) -> None:
    chrome.find_element(By.ID, "tilesCanvas_mixerTemp1").click()
    current_temp = int(chrome.find_element(By.ID, "editParamEdValue").text)
    
    if current_temp == new_temp:
        chrome.find_element(By.ID, "editParamCancelBtn").click()
        return

    difference = new_temp - current_temp

    # difference > 0 when increasing
    # difference < 0 when decreasing
    button = None
    if difference > 0:
        button = chrome.find_element(By.ID, "editParamAddBtn")
    else:
        button = chrome.find_element(By.ID, "editParamOddBtn")

    for i in range(abs(difference)):
        button.click()

    chrome.find_element(By.ID, "editParamSaveBtn").click()
    

saved_bolder_temp = None
while True:
    all_params = get_device_parameters()
    boiler_temp = all_params["curr"]["tempCO"]

    mixer_temp = all_params["curr"]["mixerTemp1"]
    mixer_set_temp = all_params["curr"]["mixerSetTemp1"]
    mixer_pump = all_params["curr"]["mixerPumpWorks1"]
    
    cwu_temp = all_params["curr"]["tempCWU"]
    cwu_pump = all_params["curr"]["pumpCWUWorks"]

    if saved_bolder_temp is not None:
        boiler_temp_tendency = boiler_temp - saved_bolder_temp
        print(f"Boiler temp tendency {boiler_temp_tendency}*C/min") 
        if cwu_pump:
            print("CWU pump is on, do nothing")
            set_mixer_temp(30)
        else:
            if boiler_temp < 70:
                set_mixer_temp(30)
            elif abs(mixer_set_temp - mixer_temp) <= 2:
                if boiler_temp_tendency >= 0:
                    set_mixer_temp(mixer_set_temp+1)
                else:
                    set_mixer_temp(mixer_set_temp-1)

    saved_bolder_temp = boiler_temp 
    sleep(60)