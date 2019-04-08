#!/bin/bash
gunicorn app:app --daemon
python send_email_worker.py
