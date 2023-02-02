#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
## following pip dependencies are required:
###
# * RPi.GPIO
# * gpiozero
# * loguru

###
## Variable definitions
###
# which GPIO pin is used for your fan connection?
gpioPin = 17
# in which interval (seconds) should the temperature check take place?
checkInt = 30
# on which temperature the fan should start spinning?
threshold = 48
# on which difference to the threshold should the fan stop spinning again?
tmpDiff = 7
# where should the log file be placed?
logPath = "/var/log/fan.log"
# at which size should the log file be rotated?
logMaxSize = "100 MB"
# which logs should be written out to the file?
logLevel = "ERROR"

###
## library imports
###
import RPi.GPIO as GPIO
import time, os, re

from loguru import logger
from gpiozero import CPUTemperature

###
## GPIO preparation
###
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False);

GPIO.setup(gpioPin, GPIO.OUT, initial=False)
fanState = False

###
## prepare additional log file
###
logger.add(logPath, rotation=logMaxSize, level=logLevel)

###
## Temperature monitoring and fan control
###
logger.info("Service started.")
while True:
    # GPU temperature
    GPUtemp = os.popen('vcgencmd measure_temp').readline()
    t1 = float(re.search('^.*?([0-9]+(\.[0-9]+)).*$', GPUtemp).group(1))
    # CPU temperature
    t2 = CPUTemperature().temperature
    # control fan
    if (
        fanState == False and (
            t1 >= threshold or
            t2 >= threshold
        )
    ):
        try:
            GPIO.output(gpioPin, True)
            fanState = True
            logger.info("STARTED fan with GPU temp {g} and CPU temp {c}".format(g=t1, c=t2))
        except Exception as e:
            logger.exception("Error while turning ON fan:")
    elif (
        fanState == True and
        t1 < (threshold - tmpDiff) and
        t2 < (threshold - tmpDiff)
    ):
        try:
            GPIO.output(gpioPin, False)
            fanState = False
            logger.info("STOPPED fan with GPU temp {g} and CPU temp {c}".format(g=t1, c=t2))
        except Exception as e:
            logger.exception("Error while turning OFF fan:")
    time.sleep(checkInt)
