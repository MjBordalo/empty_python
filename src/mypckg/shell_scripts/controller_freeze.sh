#!/bin/bash

# Review 11 Ago 2020 by @mjbordalo

# this screen should be called peiodically by crontab
# it checks the last modified time of a file created in side a temporary folder (tipically a link to  a folder in ram memmory)
# if the time exceeds a threshold this means the software is not responding and should be killed and re-lanched
#crontab example:   * * * * * bash /home/pi/firespot/src/versatile/shell_scripts/controller_freeze.sh -d 300 -t _cameraN -c "bash /home/pi/firespot/scripts/start_up_edit.sh"
INGEN="cscreen"
LIMIT_DELAY=300
NAME=""
COMMAND=""

#Parse arguments
#for i in "$@"
#do
#case $i in
#    -d=*|--delay=*)
#    LIMIT_DELAY="${i#*=}"
#    shift # past argument=value
#    ;;
#    -t=*|--text=*)
#    NAME="${i#*=}"
#    shift # past argument=value
#    ;;
#    -c=*|--command=*)
#    COMMAND="${i#*=}"
#    shift # past argument=value
#    ;;
#esac
#done

while getopts d:t:c: option 
do 
 case "${option}" 
 in 
 d) LIMIT_DELAY=${OPTARG};; 
 t) NAME=${OPTARG};; 
 c) COMMAND=${OPTARG};; 
 esac 
done 

echo "INPUTS"
echo "LIMIT_DELAY: $LIMIT_DELAY"
echo "NAME: $NAME"
echo "COMMAND: $COMMAND"

LAST_MOD="$(find /tmpfolder/freeze$NAME.txt -printf '%C@\n')"
LAST_TIME=${LAST_MOD%.*}
CURRENT_EPOCH=$( date +%s )
DELAY="$(( $CURRENT_EPOCH - LAST_TIME ))"

if (( $DELAY < $LIMIT_DELAY ))
then
    echo "Everything fine."
else
    echo $(date)"  :: $S FROZEN :: $LAST_TIME : $DELAY " >> /home/pi/frozen.csv
    #for pid in $(pgrep -f $INGEN); do kill -9 $pid; done
    #sudo /usr/bin/screen -wipe
	  #sudo bash /home/pi/edp-controller/crontab_scripts/camera_setup.sh
    #sudo /usr/bin/screen -d -m -S $INGEN -L sudo python3 -m $module
    eval $COMMAND
fi
