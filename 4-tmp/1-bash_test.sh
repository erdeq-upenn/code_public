#!/bin/bash -x 
#########################
#       usage: bash 1-bash_test.sh
#########################

export MYDIR=$PWD
#export MYDATE=$(date + %Y%m%d)
export MYDT=$(date +"%Y%m%d_%H%M%S")


#echo $MYDIR
#echo "MYDT = $MYDT"

echo "Starting pulling data from TD api..."
ff="$MYDIR/tickers.txt"
for MYTICKER in AMD APPL
do 
    echo "===================================="
    echo "Starting pulling $MYTICKER"
    echo "===================================="
    echo $(date)
    # python somefile.py >> $LOGDIR/name_${MYDT}.log 2>&1 &
done
echo "All finished"
