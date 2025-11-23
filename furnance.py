import datetime as dt
from utils import *
from states import *

login("", "")

update_device_parameters()
boiler_old_temp = dp.boiler_temp
boiler_gain_temp = dp.boiler_temp

boiler_temp_direction = int(-1)
while True:
    update_device_parameters()
    
    if boiler_gain_temp > 0.01 and boiler_temp_direction < 4:
        boiler_temp_direction += 1
    elif boiler_gain_temp < -0.01 and boiler_temp_direction > -4:
        boiler_temp_direction -= 1
        
    if dp.boiler_temp < 70 and dp.cwu_pump:
        set_mixer_temp(30)
    elif dp.boiler_temp < 70:
        set_mixer_temp(35)
    else:
        if boiler_temp_direction == 4:
            set_mixer_temp(dp.mixer_set_temp + 1)
            boiler_temp_direction = 0
        if boiler_temp_direction == -4:
            set_mixer_temp(dp.mixer_set_temp - 1)
            boiler_temp_direction = 0

    boiler_gain_temp = round(dp.boiler_temp - boiler_old_temp, 3)
    boiler_old_temp = dp.boiler_temp
    print(f"{dt.datetime.now()}: Boiler current temp {dp.boiler_temp}*C, Boiler gain: {boiler_gain_temp} *C, Temp direction {boiler_temp_direction}")
    sleep(30) 