from PyQt5 import QtWidgets, QtCore
import sys
from src.ApplicationWindow import ApplicationWindow
import argparse
from pymavlink import mavutil
import os
from datetime import datetime
from pathlib import Path

DEFAULT_PATH = os.path.join(os.getcwd(), "logs")

if __name__ == "__main__":
    # read command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, help="enter virtual port, eg. COM14",
                        nargs='?', default='COM14', const=0)
    port = parser.parse_args().port

    # setup connection via mavlink
    master = mavutil.mavlink_connection(port)
    master.wait_heartbeat()
    master.mav.param_request_list_send(master.target_system, master.target_component)
    print("Connection established.")

    # get path for logs
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    dt_string += ".csv"
    log_path = Path(os.path.join(DEFAULT_PATH, dt_string))

    # run app
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(master, log_path)
    app.show()
    qapp.exec_()
