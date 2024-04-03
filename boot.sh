#!/bin/bash
flask db upgrade
exec gunicorn -b :5001 --access-logfile - --error-logfile - lunch:app