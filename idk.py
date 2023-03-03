import mysql.connector
from names import names
from datetime import datetime
import random as r

import random
import time
    
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)
    
print(random_date("2001-01-01", "2010-01-01", random.random()))


import mysql.connector
from names import names
from datetime import datetime
import random as r
cnx = mysql.connector.connect(user='root', password='password',host='127.0.0.1',database='youtube')
cursor = cnx.cursor()
created_at_query = ("UPDATE videos set created_at = %s"
             "where id = %s")

for i in range(1,508):
	date_of_birth = (random_date("1970-01-01", "2023-02-27", random.random()), i)
	cursor.execute(date_of_birth_query, date_of_birth)
	print(cursor.statement)


cnx.commit()





