__author__ = 'suren'

class SerialData:

    court_no = 10
    curr_state = "INV"
    def __init__(self, ser):
        tokens = ser.split("-")
        pin_token = tokens[1]
        state_token = tokens[2]
        self.court_no = int(pin_token[4])
        state_str = int(state_token[11])
        # print "state_str"
        # print state_str
        if state_str == 1:

            self.curr_state = "ON"
            # print "in 1 ****"
            # print self.curr_state
        elif state_str == 0:
            self.curr_state = "OFF"
            # print "in 0 ^^^^^"
            # print self.curr_state
