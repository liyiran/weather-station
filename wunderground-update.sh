#!/bin/bash -ex

BASEDIR=$(dirname "$0")
KEY=`cat $BASEDIR/open-weather-api.key`
COORD=5392952 # Santa Barbara

curl -s -G \
	-o ${BASEDIR}/open-weather-conditions-data.json \
	"api.openweathermap.org/data/2.5/weather?id=${COORD}&appid=${KEY}"

sleep 1

curl -s -G \
	-o ${BASEDIR}/open-weather-forecast-data.json \
	"api.openweathermap.org/data/2.5/forecast?id=${COORD}&appid=${KEY}"
