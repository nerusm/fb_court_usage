__author__ = 'suren'

class Court_usage:

    def __init__(self, court_no, curr_state, start_time, end_time, run_time, row_id):
        self.court_no = court_no
        self.curr_state = curr_state
        self.start_time = start_time
        self.end_time = end_time
        self.run_time = run_time
        self.row_id = row_id

    def __repr__(self):
        return '<Court Usage RowID:{}, Court No: {}, Start Time: {}, End Time: {}, Run Time: {}, Curr State: {}>'.\
            format(self.row_id, self.court_no, self.start_time, self.end_time, self.run_time, self.curr_state)
