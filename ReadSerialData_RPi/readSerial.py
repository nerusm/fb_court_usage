import serial
# import RPi.GPIO as GPIO
import datetime
from datetime import timedelta
import time
import threading
from DBHelper import DBHelper
from Models.Court_usage import Court_usage
from Models.serial_data import SerialData



def write_to_database(serial_string, end_time):
    # print serial_data
    # tokens = serial_data.split("-")
    # # print st + ":: " + "-".join(tokens[1:3])
    serial_data = SerialData(serial_string)

    court_no = int(serial_data.court_no)
    curr_state = serial_data.curr_state
    # print serial_data.court_no
    # print serial_data.curr_state

    dbh = DBHelper()

    if curr_state == "ON":
        court_occupied = check_if_court_occupied(court_no)
        if not court_occupied:
            court_usage = Court_usage(court_no, "OCC", time.strftime('%Y-%m-%d %H:%M:%S'),
                                  time.strftime('%Y-%m-%d %H:%M:%S'), "00:00:00",0)
            dbh.insert_court_usage(court_usage)
        else:
            print "Court Already Occupied:", court_occupied
    elif curr_state == "OFF":
        # court_usage = Court_usage(court_no, "ON", time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S'), 0,0)
        court_occupied = check_if_court_occupied(court_no)
        if court_occupied:
            print "Court Selected From Table: ", court_occupied
            court_usage = calculate_runtime(court_occupied,end_time)
            print "Update Court Usage Object: ", court_usage
            dbh.update_court_usage(court_usage)
        else:
            print "Error:: No Record Found to Update For CourtNo: ", court_no," at ", end_time

# write_to_database("STATE_CHANGE-PIN=1-CURR_STATE=0", time.strftime('%Y-%m-%d %H:%M:%S' ))
def calculate_runtime(court_usage, end_time):
    start_time = court_usage.start_time
    print "ST: ",type(start_time)
    print "ET: ", type(end_time)
    # start_time_object = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S' )
    end_time_object = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    run_time = end_time_object - start_time
    print "Run Time: ", run_time
    print "RT: ", type(run_time)
    court_usage.end_time = end_time
    court_usage.curr_state = "OPEN"
    court_usage.run_time = str(run_time)
    return court_usage

def check_if_court_occupied(court_no):
    dbh = DBHelper()
    court_usage1 = dbh.get_court_usage(court_no)
    if court_usage1:
        # print court_usage1
        return court_usage1
    else:
        print("No Court ")
        return

def pre_check():
    print "Commence Pre-Check"
    try:
        print "Checking Serial Port If Is Open..."
        serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
    except Exception as e:
        print("Exception in Pre-Check: ",e)
        exit(0)
def conv_str_timedelta(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    time_delta_obj = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
    return time_delta_obj

print "Waiting..."
time.sleep(10)
print "Ready"
try:
    pre_check()
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    ser.flushInput()
    KEY_WORD = "STATE_CHANGE-PIN="
    while True:
        # if not ser.is_open:
        #     ser.open()

        # if ser.readable():
        # read_ser = ser.readline()[:-2]
        read_ser = ser.readline()

        # print read_ser
        if read_ser:
            if read_ser.startswith(KEY_WORD):
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                # print "HI"
                print read_ser
                print(st + ":: " + read_ser)
                t1 = threading.Thread(target=write_to_database, args=(read_ser, st,))
                t1.start()
            # ser.close()
            # else:
            #     print "Serial Read System Not Ready; Retry again"
            # else:
            # "Not readable"
    # ser.close()

except Exception as e:
    print(e)

finally:
    print "Closing Port"
    ser.close()




