#!/bin/bash
gunicorn -w 4 -t 3600 -b 0.0.0.0:5000 main:app
