__author__ = 'suren'
import MySQLdb
from datetime import datetime, timedelta
from Models.Court_usage import Court_usage


class DBHelper:
    last_update_row_id = 0;
    def getConn(self):
        print "Openning DB Connection..."
        db = MySQLdb.connect("localhost", "pi_user", "raspberry", "FB_MANAGE_V01")
        print "DB Connection opened..."
        sql = "UPDATE sequence SET id=LAST_INSERT_ID(id+1);"
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()

        except Exception, e:
            db.rollback()
            print 'Caught Exception: %s' % e

        return db

    def update_court_usage(self,court_usage):
        status = 0;
        court_usage_update_sql = "UPDATE court_usage SET curr_state = '%s', end_time = '%s', run_time = '%s' WHERE row_id = %s" %\
                                    ("CLOSED", court_usage.end_time, court_usage.run_time, court_usage.row_id)
        # court_usage_update_sql = "UPDATE court_usage SET curr_state = '%s', end_time = '%s', run_time = '%s' WHERE row_id = %s" % \
        #                          (
        #                          court_usage.curr_state, court_usage.end_time, court_usage.run_time, court_usage.row_id)
        # courts_update_sql = "UPDATE courts SET curr_state = '%s' WHERE court_no = %s" % (court_usage.curr_state, court_usage.court_no)
        # courts_update_sql = "UPDATE courts SET curr_state = '%s' WHERE court_no = %s" % (court_usage.curr_state, court_usage.court_no)
        print "court_usage Update SQL: ", court_usage_update_sql

        db = self.getConn()
        cursor = db.cursor()
        try:
            cursor.execute(court_usage_update_sql)
            cursor.execute("SELECT total_run_time FROM courts where court_no = %s" % (court_usage.court_no))
            result = cursor.fetchone()
            rtime_str = result[0]
            table_runtime_delta_obj = conv_str_timedelta(rtime_str)
            runtime_delta_obj = conv_str_timedelta(court_usage.run_time)
            total_run_timedelta_obj = table_runtime_delta_obj + runtime_delta_obj
            courts_update_sql = "UPDATE courts SET curr_state = '%s', total_run_time = '%s'  WHERE court_no = %s" % (
                court_usage.curr_state, str(total_run_timedelta_obj), court_usage.court_no)
            print("courts Update SQL: ", courts_update_sql)
            cursor.execute(courts_update_sql)
            db.commit()
            print "Court Usage & Courts table Updated.."

        except Exception, e:
            db.rollback()
            print 'Caught Exception: %s' % e.__str__()
            status = 1;
        finally:
            db.close()
        return status




    def insert_court_usage(self, Court_usage):
        status = 0;
        self.get_lastest_rowid()
        sql = "INSERT INTO court_usage (court_no, curr_state, start_time, end_time, run_time, row_id) values " \
              "('%s','%s','%s','%s','%s', %s)" % (
                  Court_usage.court_no, Court_usage.curr_state, Court_usage.start_time, Court_usage.end_time,
                  Court_usage.run_time, self.last_update_row_id)
        courts_update_sql = "UPDATE courts SET curr_state = '%s' WHERE court_no = %s" % (Court_usage.curr_state, Court_usage.court_no)
        print("Update SQL while insert: ",courts_update_sql)
        db = self.getConn()
        cursor = db.cursor()
        print "SQL: ", sql
        try:
            cursor.execute(sql)

            cursor.execute(courts_update_sql)
            db.commit()
            print "Court Usage record inserted into table.."

        except Exception, e:
            db.rollback()
            print 'Caught Exception: %s' % e
            status = 1;
        finally:
            db.close()
        return status

    def get_court_usage(self, court_no):
        status = 0;
        sql = "SELECT * FROM court_usage WHERE curr_state = 'OCC' AND court_no = %s " % (court_no);
        db = self.getConn()
        cursor = db.cursor()
        print sql
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                for row in results:
                    court_no = row[0]
                    curr_state = row[1]
                    start_time = row[2]
                    end_time = row[3]
                    run_time = row[4]
                    row_id = row[5]
                court_usage = Court_usage(court_no, curr_state, start_time, end_time, run_time, row_id)
                return court_usage
            else:
                return
        except Exception, e:
            db.rollback()
            print 'Caught Exception: %s' % e
            status = 1;
        finally:
            print "DB Close"
            db.close()





    def get_lastest_rowid(self):
        db = self.getConn()
        cursor = db.cursor()
        try:
            sql1 = "SELECT * FROM sequence"
            cursor.execute(sql1)
            results = cursor.fetchall()
            # print results
            for row in results:
                self.last_update_row_id = int(row[0]) + 1
            print "Sequence Updated"
            print self.last_update_row_id
        except Exception, e:
            db.rollback()
            print 'Caught Exception: %s' % e
        finally:
            db.close()

def conv_str_timedelta(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    time_delta_obj = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
    return time_delta_obj