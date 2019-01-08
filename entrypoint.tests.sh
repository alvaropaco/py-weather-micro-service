#!/bin/bash
service rabbitmq-server start
nameko run weather_service &
nose2