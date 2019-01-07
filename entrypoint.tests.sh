#!/bin/bash
service rabbitmq-server start
nameko run zipcode &
nose2