import json
import pingparsing
from datetime import datetime
import mysql.connector

from functions import get_environment_variable




mydb = mysql.connector.connect(
  host="192.168.0.162",
  user = get_environment_variable('NETWORKMONITOR_MYSQL_USER'),
  password= get_environment_variable('NETWORKMONITOR_MYSQL_PASS'),
  database="network_connectivity"
) 
mycursor = mydb.cursor()



ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()
transmitter.destination = "8.8.8.8"
transmitter.count = 4
result = transmitter.ping()
result_dict = ping_parser.parse(result).as_dict()


now = datetime.now()
time = now.strftime("%Y-%m-%d %H:%M:%S")

ip_address = result_dict["destination"]

if result_dict["packet_loss_count"] == 0:
    success = "1"
else:
    success = "0"



rtt = int(result_dict["rtt_avg"])


sql = 'INSERT INTO network_connectivity.pings (time, ip_address, success, rtt) VALUES ("%s", "%s", %s, %s);' % (time, ip_address, success, rtt)
print(sql)

try:
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))