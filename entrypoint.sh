#!/bin/bash
service rabbitmq-server start
nameko run zipcode &
python api.py