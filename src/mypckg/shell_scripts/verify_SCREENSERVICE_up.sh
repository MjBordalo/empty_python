#!/usr/bin/bash
# usually this script is called periodically from crontab:
#Example:
#* * * * * sudo bash /home/pi/verify_SCREENSERVICE_up.sh


SERVICE="service-screen"
if (( $(pgrep -f $SERVICE | wc -l) >= 1 ))
then
echo "Not starting screen"
echo $SERVICE" is up (individual)"
exit 1
else
echo "Starting screen"

#Method1
cd /home/pi/irrigation_controller/src/
#/usr/bin/screen -L -dmS $SERVICE /usr/bin/python3 main.py
# sudo /usr/bin/screen -d -m -S $INGEN -L sudo python2 /home/pi/edp-gateway/src/main.py
#Method2
# screen -dmS $SERVICE
# #the stuff command allows you to wirte on a sreen. so we write commands and press enter simulating user interection
# screen -x $SERVICE -X stuff "cd /home/pi/guardian-local/src^M"   #the ^M is extemely importat its like an ENTER char like /n
# screen -x $SERVICE -X stuff "sudo /usr/bin/python3.5 main.py^M"
# # /usr/bin/screen -L -dmS $SERVICE sudo /usr/bin/python3.5 main.py
fi
