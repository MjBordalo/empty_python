#!/bin/bash
#This is a script global to any client. you just have to make sure to call it has:
# cd (...)/mqtt-python-server/src && bash client-restart.sh -n="CLIENTNAME"
# where CLIENTNAME shoud be the name of the folder inside /src

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CLIENTNAME="NONAME"
#Parse arguments
for i in "$@"
do
case $i in
    -n=*|--client_name=*)
    CLIENTNAME="${i#*=}"
    shift # past argument=value
    ;;
esac
done

SERVICE=$CLIENTNAME"-mqtt-client"
if (( $(pgrep -f $SERVICE | wc -l) >= 1 ))
then
exit 1
else
for pid in $(pgrep -f $SERVICE); do kill -9 $pid; done
/usr/bin/screen -d -m -S $SERVICE -L python3 -m $CLIENTNAME.$CLIENTNAME"_client"
fi
