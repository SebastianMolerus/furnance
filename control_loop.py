import datetime as dt
from operations import *
from pid import *
login("", "") 
H2_boiler_temp = 65
p = pid(67.5, 1, 1, 2)

while True:
    update_device_parameters()

    if dp.cwu_pump and dp.boiler_temp < H2_boiler_temp:
        set_mixer_temp(30)
        print(f"{dt.datetime.now()}: CWU Pump is working, nothing to do")
    else:
        pid_output = round(p.control(dp.boiler_temp), 3)
        
        if pid_output > 0:
            change_mixer_temp(False)
        elif pid_output < 0:
            change_mixer_temp(True)

        print(f"{dt.datetime.now()}: Boiler current temp {dp.boiler_temp}*C, PID: {pid_output}")

    sleep(90) 