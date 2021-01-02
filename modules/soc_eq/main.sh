#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
socDebug=1


case $CHARGEPOINT in
  2)
    # second charge point
    ladeleistungfile="$RAMDISKDIR/llaktuells1"
    soctimerfile="$RAMDISKDIR/soctimer1"
    soc_file="$RAMDISKDIR/soc1"
    soc_eq_client_id=$soc_eq_client_id_lp2
    soc_eq_client_secret=$soc_eq_client_secret_lp2
    soc_eq_vin=$soc_eq_vin_lp2
    ;;
  *)
    # defaults to first charge point for backward compatibility
    # set CHARGEPOINT in case it is empty (needed for logging)
    CHARGEPOINT=1
    ladeleistungfile="$RAMDISKDIR/llaktuell"
    soctimerfile="$RAMDISKDIR/soctimer"
    soc_file="$RAMDISKDIR/soc"
    soc_eq_client_id=$soc_eq_client_id_lp1
    soc_eq_client_secret=$soc_eq_client_secret_lp1
    soc_eq_vin=$soc_eq_vin_lp1
    ;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date --rfc-3339=seconds`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimer=$(<$soctimerfile)
ladeleistung=$(<$ladeleistungfile)

if (( ladeleistung > 500 ));then
  tmpintervall=$(( 5 * 6 ))
else
  tmpintervall=$(( 60 * 6 ))
fi
  #tmpintervall=5

if (( soctimer < tmpintervall )); then
  socDebugLog "Nothing to do yet. Incrementing timer. ${soctimer} < ${tmpintervall}"
  soctimer=$((soctimer+1))
  echo $soctimer > $soctimerfile
else
  socDebugLog "Requesting SoC"
  #export soc_eq_client_id soc_eq_client_secret soc_eq_vin soc_file CHARGEPOINT
  #$MODULEDIR/soc.py 
  $MODULEDIR/soc.py $soc_eq_client_id $soc_eq_client_secret $soc_eq_vin $soc_file $CHARGEPOINT >>$LOGFILE &
  
  echo 0 > $soctimerfile
fi

