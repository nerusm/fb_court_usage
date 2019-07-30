__author__ = 'suren'
from DBHelper import DBHelper
from Models.Court_usage import Court_usage
import time

def write_to_database(serial_data, st):
    tokens = serial_data.split("-")
    print st + ":: " + "-".join(tokens[1:3])
    court_usage = Court_usage(1, "OCC", time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S'), 0)
    dbh = DBHelper()
    dbh.insert_court_usage(court_usage)


write_to_database("STATE_CHANGE-PIN=1-CURR_STATE=0", time.strftime('%Y-%m-%d %H:%M:%S' ))