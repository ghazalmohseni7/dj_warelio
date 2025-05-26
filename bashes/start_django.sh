#!/bin/bash
echo "Starting Gunicorn..."
exec gunicorn dj_warelio.wsgi:application -b 0.0.0.0:8001