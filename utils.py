from selenium.webdriver import *
from selenium.webdriver.common.by import By
import json
from time import sleep

paramRequest = "https://www.econet24.com/service/getDeviceParams?uid=AFGPPB0Z32D1P148G02G0&_=1763824107482"
mainPage = "https://www.econet24.com/main/"

class device_parameters:
    boiler_temp = float()

    mixer_temp = float()
    mixer_set_temp = int()
    mixer_pump = bool()

    cwu_temp = float()
    cwu_pump = bool()

global dp
dp = device_parameters()

def get_device_parameters() -> json:
    chrome.get(paramRequest)
    elem = chrome.find_element(By.TAG_NAME, "pre")
    son = json.loads(elem.text)
    chrome.back()
    return son

def login(user: str, pw: str) -> None:
    global chrome 
    chrome = Chrome()
    chrome.minimize_window()
    chrome.get(mainPage)

    user_name = chrome.find_element(By.ID, "username")
    user_name.send_keys(user)

    password = chrome.find_element(By.ID, "password")
    password.send_keys(pw)

    login_button = chrome.find_element(By.ID, "btnLogin")
    login_button.click()
    sleep(5)

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

def update_device_parameters() -> None:
    all_params = get_device_parameters()
    dp.boiler_temp = round(all_params["curr"]["tempCO"], 3)

    dp.mixer_temp = round(all_params["curr"]["mixerTemp1"], 3)
    dp.mixer_set_temp = all_params["curr"]["mixerSetTemp1"]
    dp.mixer_pump = all_params["curr"]["mixerPumpWorks1"]
    
    dp.cwu_temp = round(all_params["curr"]["tempCWU"], 3)
    dp.cwu_pump = all_params["curr"]["pumpCWUWorks"]