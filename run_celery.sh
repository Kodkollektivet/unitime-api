#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -c "celery -A settings worker -l info -B"
#su -c "celery -A settings worker -l info &"
