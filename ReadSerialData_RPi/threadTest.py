__author__ = 'suren'
import threading
import time

def print_num(num):
    print "inside thread function, going to sleep"
    time.sleep(num)
    print "thread awake"


if __name__ == "__main__":
    t1=threading.Thread(target=print_num,args=(10,))
    t1.start()
    # t1.join()
    print "thread started"


    print "Done"
