#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A src.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery -A src.tasks.tasks:celery flower
 fi