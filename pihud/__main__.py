
import os
import sys
import obd
import shutil
import logging
import pika
from PiHud import PiHud
from PyQt5 import QtGui, QtWidgets
from GlobalConfig import GlobalConfig
from rmqpublisher import RMQPublisher

try:
    import RPi.GPIO as GPIO
except:
    print("[pihud] Warning: RPi.GPIO library not found")

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


# file paths
running_dir         = os.path.dirname(os.path.realpath(__file__))
default_config_path = os.path.join(running_dir, 'default.rc')
config_path         = os.path.join(os.path.expanduser('~'), 'pihud.rc')

# custom font
custom_font_path    = os.path.join(running_dir, 'fonts/digital-dismay/Digital Dismay.otf')

def main():
    """ entry point """

    # ============================ Config loading =============================

    if not os.path.isfile(config_path):
        # copy the default config
        if not os.path.isfile(default_config_path):
            print("[pihud] Fatal: Missing default config file. Try reinstalling")
            sys.exit(1)
        else:
            shutil.copyfile(default_config_path, config_path)

    global_config = GlobalConfig(config_path)
    global_config["custom_font"] = custom_font_path

    # =========================== OBD-II Connection ===========================

    if global_config["debug"]:
        obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    connection = obd.Async(global_config["port"])

    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    rmq = RMQPublisher(global_config["rmq_conn"])

    global_config["rmqpublisher"] = rmq

    try:
        rmq.run()
    except KeyboardInterrupt:
        rmq.stop()

    # if global_config["debug"]:
    #     for i in range(32):
    #         connection.supported_commands.append(obd.commands[1][i])

    # ============================ QT Application =============================

    app = QtWidgets.QApplication(sys.argv)
    pihud = PiHud(global_config, connection)

    # ============================== GPIO Setup ===============================

    try:
        pin = self.config.page_adv_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,
                   GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)
        GIO.add_event_detect(pin,
                             GPIO.FALLING,
                             callback=pihud.next_page,
                             bouncetime=200)
    except:
        pass

    # ================================= Start =================================

    status = app.exec_() # blocks until application quit

    # ================================= Exit ==================================
    connection.close()
    sys.exit(status)


if __name__ == "__main__":
    main()
