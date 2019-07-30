#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import MySQLdb

db = MySQLdb.connect("localhost", "pi_user", "raspberry", "FB_MANAGE_V01")
cursor = db.cursor()
ls = "LAST_INSERT_ID(id+1)"
sql = "UPDATE sequence SET id = %s" % (ls)
print "SQL: ", sql
try:
    cursor.execute(sql)
    db.commit()
    print "Court Usage record inserted into table.."

except Exception, e:
    db.rollback()
    print 'Caught Exception: %s' % e
    status = 1;
finally:
    db.close()
