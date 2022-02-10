import PySimpleGUI as sg
import time
import sys
import argparse
from pymavlink import mavutil
from utils import recalculate_current
from random import random

# read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, help="enter virtual port, eg. COM14",
                    nargs='?', default='COM14', const=0)
port = parser.parse_args().port

# establish connection via mavlink
master = mavutil.mavlink_connection(port)
master.wait_heartbeat()
master.mav.param_request_list_send(master.target_system, master.target_component)

# create window layout
sg.ChangeLookAndFeel('SandyBeach')
sg.SetOptions(element_padding=(0, 0))

layout = [[sg.Text('')],
          [sg.Text('Power Monitor', font=('Times New Roman', 30, 'bold'))],
          [sg.Text(font=('Times New Roman', 30), key='voltage')],
          [sg.Text(font=('Times New Roman', 30), key='current')],
          [sg.Exit(button_color=('black', 'firebrick4'), key='Exit')]]

window = sg.Window('Battery Monitor', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                   grab_anywhere=True, element_justification='c')

# set default values
voltage = 0
raw_current = 0
current = 0

# main loop
while True:
    time.sleep(0.1)
    # try reading value via mavlink
    try:
        message = master.recv_match(type='SYS_STATUS', blocking=True).to_dict()
        voltage = message['voltage_battery'] / 1000
        raw_current = message['current_battery'] / 100
        current = recalculate_current(raw_current)
    except Exception as error:
        print(error)
        sys.exit(0)
    # update window
    event, values = window.read(timeout=10)
    window['voltage'].update("Voltage: {:.4f} V".format(round(voltage, 4)))
    window['current'].update("Current: {:.4f} A".format(round(current, 4)))

    if event == 'Exit':
        break
