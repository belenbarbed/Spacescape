#!/bin/bash

re=$'id=([0-9])\t'
devices=$(xinput list | grep "SIGMACHIP" | grep "slave  keyboard")

if [[ $devices =~ $re ]] ; then
	if [[ $1 = "enable" ]] ; then
		xinput enable ${BASH_REMATCH[1]}
	fi
	if [[ $1 = "disable" ]] ; then
		xinput disable ${BASH_REMATCH[1]}
	fi
fi		
