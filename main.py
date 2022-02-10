from PyQt5 import QtWidgets, QtCore
import sys
from src.ApplicationWindow import ApplicationWindow
import argparse
from pymavlink import mavutil


if __name__ == "__main__":
    # read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, help="enter virtual port, eg. COM14",
                        nargs='?', default='COM14', const=0)
    port = parser.parse_args().port

    # setup connection via mavlink
    #master = mavutil.mavlink_connection(port)
    # master.wait_heartbeat()
    # master.mav.param_request_list_send(master.target_system, master.target_component)
    master = 1
    print("Connection established.")

    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow(master)
    app.show()
    qapp.exec_()
