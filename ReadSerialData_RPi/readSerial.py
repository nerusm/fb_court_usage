import serial
# import RPi.GPIO as GPIO
import datetime
from datetime import timedelta
import time
import threading
from DBHelper import DBHelper
from Models.Court_usage import Court_usage
from Models.serial_data import SerialData
import logging.config
import logging

serialName = "/dev/ttyACM0"
# serialName = "/dev/tnt1"
baudRate = 9600
logging.config.fileConfig("logging.ini")
log = logging.getLogger(__name__)
def write_to_database(serial_string, end_time):
    serial_data = SerialData(serial_string)
    court_no = int(serial_data.court_no)
    curr_state = serial_data.curr_state
    
    dbh = DBHelper()

    if curr_state == "ON":
        court_occupied = check_if_court_occupied(court_no)
        if not court_occupied:
            court_usage = Court_usage(court_no, "OCC", time.strftime('%Y-%m-%d %H:%M:%S'),
                                  time.strftime('%Y-%m-%d %H:%M:%S'), "00:00:00",0)
            dbh.insert_court_usage(court_usage)
        else:
            log.info("Court Already Occupied:" + court_occupied.__repr__())
    elif curr_state == "OFF":
        court_occupied = check_if_court_occupied(court_no)
        if court_occupied:
            log.info("Court Selected From Table: " + court_occupied.__repr__())
            court_usage = calculate_runtime(court_occupied,end_time)
            log.info("Update Court Usage Object: " + court_usage.__repr__())
            # if (court_usage.run_time < )
            dbh.update_court_usage(court_usage)
        else:
            log.info("Error:: No Record Found to Update For CourtNo: %s at %s" , court_no, end_time)

# write_to_database("STATE_CHANGE-PIN=1-CURR_STATE=0", time.strftime('%Y-%m-%d %H:%M:%S' ))
def calculate_runtime(court_usage, end_time):
    start_time = court_usage.start_time
    log.info("Start Time: %s" , (start_time))
    log.info("End Time: %s" , (end_time))
    # start_time_object = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S' )
    end_time_object = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    run_time = end_time_object - start_time
    log.info("Run Time: %s", run_time)
    log.info("Run Time Type: %s" , (run_time))
    court_usage.end_time = end_time
    court_usage.curr_state = "OPEN"
    court_usage.run_time = str(run_time)
    return court_usage

def check_if_court_occupied(court_no):
    dbh = DBHelper()
    court_usage1 = dbh.get_court_usage(court_no)
    if court_usage1:
        return court_usage1
    else:
        log.info("Court Free")
        return

def pre_check():
    log.info("Commence Pre-Check")
    try:
        log.info("Checking Serial Port If Is Open...")
        serial.Serial(serialName, baudRate, timeout=0.5)
    except Exception as e:
        log.error("Exception in Pre-Check: ", exc_info=True)
        exit(0)
def conv_str_timedelta(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    time_delta_obj = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
    return time_delta_obj

log.info("Waiting...")
time.sleep(10)
log.info("Ready")
try:
    pre_check()
    ser = serial.Serial(serialName, baudRate, timeout=0.5)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = baudRate
    ser.flushInput()
    KEY_WORD = "STATE_CHANGE-PIN="
    while True:
        read_ser = ser.readline()
        # print read_ser
        if read_ser:
            log.info(read_ser)

            if read_ser.startswith(KEY_WORD):
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                log.info(st + ":: " + read_ser)
                t1 = threading.Thread(target=write_to_database, args=(read_ser, st,))
                t1.start()
            else:
                log.info(read_ser)
            # ser.close()
            # else:
            #     print "Serial Read System Not Ready; Retry again"
            # else:
            # "Not readable"
    # ser.close()

except Exception as e:
    log.error("Exception occured: ", exc_info=True)

finally:
    log.info("Closing Port")
    ser.close()



